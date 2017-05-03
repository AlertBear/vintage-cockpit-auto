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


def get_nic_from_ip(ip, user="root", password="redhat"):
    with settings(
            warn_only=True, host_string=user + '@' + ip, password=password):
        cmd = "ip a s|grep %s" % ip
        output = run(cmd)
        nic = output.split()[-1]
        return nic


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


if __name__ == "__main__":
    # Parse variable from json file export by rhvh auto testing platform
    http_json = "/tmp/http.json"
    with open(http_json, 'r') as f:
        r = json.load(f)
    profiles = r["test_profile"]
    host_ip = r["host_ip"]
    test_build = r["test_build"]
    test_scenarios = []
    for profile in profiles:
        for c in getattr(test_scen, profile)["CASES"]:
            test_scenarios.append(c)

    # Wait for the host is ready
    i = 0
    while True:
        if i > 60:
            print "ERROR: Host is not ready for testing"
            sys.exit(1)
        with settings(warn_only=True):
            output = local("ping -c5 -W5 %s" % host_ip, capture=True)
        if output.failed:
            time.sleep(10)
            i += 1
            continue
        break

    # All files used
    abspath = os.path.abspath(os.path.dirname(__file__))
    if re.search("v41", test_scenarios[0]):
        conf_file = os.path.join(abspath, "tests/v41/conf.py")
    elif re.search("v40", test_scenarios[0]):
        conf_file = os.path.join(abspath, "tests/v40/conf.py")

    test_files = []
    for each_file in test_scenarios:
        test_file = os.path.join(abspath, each_file)
        test_files.append(test_file)

    test_files_str = " ".join(test_files)

    log_dir = os.path.join(abspath, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    result_json = log_dir + "/cockpit-result.json"
    result_html = log_dir + "/cockpit-result.html"

    # Get the mapped device of the host_ip,
    # which will be used for test_he_install.py
    host_nic = get_nic_from_ip(host_ip)

    # Modify the variable value in the config file
    variable_dict = {
        "HOST_IP": host_ip,
        "NIC": host_nic,
        "TEST_BUILD": test_build
    }
    modify_config_file(conf_file, variable_dict)

    # Execute to do the tests
    pytest.main("-s -v %s --json=%s --html=%s" % (
        test_files_str, result_json, result_html))

    # Rename the result files in case be deleted
    now = time.strftime("%y%m%d%H%M%S")
    json_result_rename = log_dir + "/cockpit-result-" + now + ".json"
    os.rename(result_json, json_result_rename)
    html_result_rename = log_dir + "/cockpit-result-" + now + ".html"
    os.rename(result_html, html_result_rename)

    # Save the screenshot during the tests to log_dir
    if os.path.exists("/tmp/cockpit-screenshot"):
        shutil.move("/tmp/cockpit-screenshot", log_dir + "/screenshot-" + now)

    # Send email to administrator
    email_subject = "Test Report For Cockpit-ovirt-%s" % now
    email_from = "dguo@redhat.com"
    email_to = ["dguo@redhat.com"]

    if not os.path.exists(log_dir + "/screenshot-" + now):
        email_text = "1. Please see the Test Report of " \
                     "Cockpit-ovirt at http://10.66.148.10:8000/%s" % \
                     "cockpit-result-" + now + ".html"
    else:
        email_text = "1. Please see the Test Report of " \
                     "Cockpit-ovirt at http://10.66.148.10:8000/{html_name} \n" \
                     "2. Please see the screenshot during the " \
                     "test at http://10.66.148.10:8000/{screenshot_name}".format(
                      html_name="cockpit-result-" + now + ".html",
                      screenshot_name="screenshot-" + now)

    email = EmailAction()
    email_attachment = []
    email.send_email(
        email_from, email_to, email_subject, email_text, email_attachment)

    # Loads the results to json from result_json file
    res = format_result(json_result_rename)
    pass
