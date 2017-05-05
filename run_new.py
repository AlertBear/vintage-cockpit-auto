#!/usr/bin/python2.7
import os
import sys
import time
import shutil
import json
import pytest
import re
import smtplib
import test_scen
from fabric.api import run, local, settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from SimpleXMLRPCServer import SimpleXMLRPCServer


class EmailAction(object):
    def __init__(self):
        self.smtp_server = "smtp.corp.redhat.com"

    def send_email(self, from_addr, to_addr, subject, text, attachments):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = ', '.join(to_addr)
        msg['Subject'] = subject

        msg.attach(MIMEText(text, 'plain', 'utf-8'))

        for a in attachments:
            with open(a, 'rb') as f:
                att = MIMEText(f.read(), 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(a))

                msg.attach(att)

        server = smtplib.SMTP(self.smtp_server, 25)
        # server.login(from_addr, password)
        try:
            server.sendmail(from_addr, to_addr, msg.as_string())
        finally:
            server.quit()


def modify_config_file(file, value_dict):
    # Modify test values in the config file
    for k, v in value_dict.items():
        local("""sed -i 's/%s =.*/%s="%s"/' %s""" % (k, k, v, file))


def format_result(file):
    # Parse the result from json file
    with open(file) as f:
        r = json.load(f)
    ret = {}
    format_ret = {}
    for case in r['report']['tests']:
        ret.update({case['name']: case['outcome']})

    for k, v in ret.items():
        format_k = k.split('::')[1].split('_')[1]
        if format_k == "login":
            continue
        format_ret.update({'RHEVM-' + format_k: v})
    return json.dumps(format_ret)


def upload_result_to_polarion(result):
    pass


def run01():
    # Parse variable from json file export by rhvh auto testing platform
    http_json = "/tmp/http.json"
    with open(http_json, 'r') as f:
        r = json.load(f)
    profiles = r["test_profile"]
    host_ip = r["host_ip"]
    test_build = r["test_build"]
    test_cases = []
    for profile in profiles:
        for c in getattr(test_scen, profile)["CASES"]:
            test_cases.append(c)

    # Wait for the host is ready
    i = 0
    while True:
        if i > 60:
            print "ERROR: Host is not ready for testing"
            sys.exit(1)
        with settings(
            warn_only=True, host_string='root@' + host_ip, password='redhat'):
            output = run("hostname")
        if output.failed:
            time.sleep(10)
            i += 1
            continue
        break

    # Get config files by rhvh version
    abspath = os.path.abspath(os.path.dirname(__file__))
    if re.search("v41", test_cases[0]):
        conf_file = os.path.join(abspath, "tests/v41/conf.py")
    elif re.search("v40", test_cases[0]):
        conf_file = os.path.join(abspath, "tests/v40/conf.py")

    # Test cases files which will be appended to the 'pytest' command line
    test_files = []
    for each_file in test_cases:
        test_file = os.path.join(abspath, each_file)
        test_files.append(test_file)

    # Make a dir for storing all the test logs
    now = time.strftime("%Y%m%d%H%M%S")
    profiles_str = "-".join(profiles)
    tmp_log_dir = "/tmp/cockpit-auto.logs/" + \
                  test_build + '/' + now
    if not os.path.exists(tmp_log_dir):
        os.makedirs(tmp_log_dir)

    # Modify the variable value in the config file
    variable_dict = {
        "HOST_IP": host_ip,
        "TEST_BUILD": test_build
    }
    modify_config_file(conf_file, variable_dict)

    # Execute to do the tests
    result_json = tmp_log_dir + "/result-" + profiles_str + ".json"
    result_html = tmp_log_dir + "/result-" + profiles_str + ".html"

    pytest_args = ['-s', '-v']
    for file in test_files:
        pytest_args.append(file)
    pytest_args.append("--json={}".format(result_json))
    pytest_args.append("--html={}".format(result_html))

    pytest.main(pytest_args)

    # After execute the tests, loading the json from json file
    result = format_result(result_json)

    # Save the screenshot during tests to tmp_log_dir
    has_screenshot = os.path.exists("/tmp/cockpit-screenshot")
    if has_screenshot:
        shutil.move("/tmp/cockpit-screenshot", tmp_log_dir + "/screenshot-" + now)

    # Save all the logs and screenshot to /var/www/html where httpd is already on
    http_logs_dir = "/var/www/html/" + test_build
    if not os.path.exists(http_logs_dir):
        os.makedirs(http_logs_dir)
    shutil.move(tmp_log_dir, http_logs_dir)

    # Send email to administrator
    email_subject = "Test Report For Cockpit-ovirt-%s(%s)" % (profiles_str, test_build)
    email_from = "dguo@redhat.com"
    email_to = ["dguo@redhat.com"]

    # Get local ip for email content
    with settings(warn_only=True):
        local_hostname = local("hostname --fqdn", capture=True)
        local_ip = local("host %s | awk '{print $NF}'" % local_hostname)

    email_text = "1. Please see the Test Report at http://%s/%s/%s" % (
        local_ip, test_build, now)

    email = EmailAction()
    email_attachment = []
    email.send_email(email_from, email_to, email_subject, email_text,
                     email_attachment)

    # Upload the result to polarion
    upload_result_to_polarion(result)

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("0.0.0.0", 9090))
    print "Listening on port 9090..."
    server.register_function(run01, "run01")
    server.serve_forever()
