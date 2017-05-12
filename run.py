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
        local("""sed -i 's/%s =.*/%s = "%s"/' %s""" % (k, k, v, file))


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
        if not re.search('\d+', format_k):
            continue
        format_ret.update({'RHEVM-' + format_k: v})
    return json.dumps(format_ret)


def format_result_to_jfile(raw_jfile, test_build, test_profile):
    # Load the result from json file
    with open(file) as f:
        r = json.load(f)

    raw_cases_result = {}
    fail_cases_result = {}
    pass_cases_result = {}
    total_cases_result = {}
    final_result = {}

    for case in r['report']['tests']:
        raw_cases_result.update({case['name']: case['outcome']})

    for k, v in raw_cases_result.items():
        format_k = k.split('::')[1].split('_')[1]
        if not re.search('\d+', format_k):
            continue
        if v == "passed":
            pass_cases_result.update({'RHEVM-' + format_k: v})
        elif v == "failed":
            fail_cases_result.update({'RHEVM-' + format_k: v})
        total_cases_result.update({'RHEVM-' + format_k: v})

    profile_cases = {test_profile: total_cases_result}

    pass_count = len(pass_cases_result.keys())
    fail_count = len(fail_cases_result.keys())
    total_count = len(total_cases_result.keys())
    sum_dict = {
            "build": test_build,
            "error": "",
            "errorlist": [],
            "failed": fail_count,
            "passed": pass_count,
            "total": total_count
        }
    final_result.update({test_build: profile_cases})
    final_result.update({"sum": sum_dict})

    '''
    # After all, the final result looks like below format
    final_result = {
        test_build: {
            test_profile: {

            },
        },
        "sum": {
            "build": test_build,
            "error": "",
            "errorlist": "",
            "failed": "",
            "passed": "",
            "total": ""
        }
    }
    '''
    # After format, put it back to raw json file
    with open(raw_jfile, 'w') as f:
        json.dump(final_result, f, indent=2)


def upload_result_to_polarion(result):
    pass


if __name__ == "__main__":
    # Parse variable from json file export by rhvh auto testing platform
    http_json = "/tmp/http.json"
    with open(http_json, 'r') as f:
        r = json.load(f)
    host_ip = r["host_ip"]
    test_build = r["test_build"]
    profiles = r["test_profile"]
    test_cases = []
    '''
    # Currently only support to only test the firsty profile
    for profile in profiles:
        for c in getattr(test_scen, profile)["CASES"]:
            test_cases.append(c)
    '''
    profile = r["test_profile"][0]
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
    tmp_result_jfile = tmp_log_dir + "/result-" + profiles_str + ".json"
    tmp_result_hfile = tmp_log_dir + "/result-" + profiles_str + ".html"

    pytest_args = ['-s', '-v']
    for file in test_files:
        pytest_args.append(file)
    pytest_args.append("--json={}".format(tmp_result_jfile))
    pytest_args.append("--html={}".format(tmp_result_hfile))

    pytest.main(pytest_args)

    # After execute the tests, format the result into human-readable
    format_result_to_jfile(tmp_result_jfile, test_build, profile)

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
        local_ip = local("host %s | awk '{print $NF}'" % local_hostname, capture=True)

    email_text = "1. Please see the Test Report at http://%s/%s/%s" % (
        local_ip, test_build, now)

    email = EmailAction()
    email_attachment = []
    email.send_email(email_from, email_to, email_subject, email_text,
                     email_attachment)
