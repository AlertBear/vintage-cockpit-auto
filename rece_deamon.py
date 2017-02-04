#!/usr/bin/python2.7
import redis
import os
import time
import json
import pytest
import smtplib
from tests.conf import REDIS_HOST
from fabric.api import run, local, settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class RedisAction(object):
    def __init__(self):
        self.redis_host = REDIS_HOST
        self.redis_conn = redis.StrictRedis(
            host=self.redis_host,
            port=6379,
            db=0,
            password="redhat")
        self.p = self.redis_conn.pubsub(ignore_subscribe_messages=True)
        self.p.subscribe("dell-per510-01.lab.eng.pek2.redhat.com-cockpit")

    def receive_ipaddr(self):
        msg = self.p.parse_response()
        try:
            if "redhat" in msg[-1]:
                ipaddr = msg[-1].split(",")[0]
                return ipaddr
            elif "done" in msg[-1]:
                self.p.unsubscribe()
                return 2
        except Exception as e:
            print e
            return 1

    def test_connection(self, ipaddr):
        with settings(host_string='root@' + ipaddr, password="redhat"):
            run("hostname")

    def publish_result(self, data):
        self.redis_conn.publish(
            "dell-per510-01.lab.eng.pek2.redhat.com-cockpit-result",
            str(data))


class EmailAction(object):
    def __init__(self):
        self.smtp_server = "smtp.corp.redhat.com"

    def send_email(
        self,
        from_addr,
        to_addr,
        subject,
        text,
        attachments):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
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


def format_result(file):
    # Parse the result and pass to redis channel
    with open(file) as f:
        r = json.load(f)
    ret = {}
    format_ret = {}
    for case in r['report']['tests']:
        ret.update({case['name']: case['outcome']})
    print ret

    for k, v in ret.items():
        format_k = k.split('::')[1].split('_')[1]
        if format_k == "login":
            continue
        format_ret.update({'RHEVM-' + format_k: v})
    return json.dumps(format_ret)


if __name__ == "__main__":
    # All files used
    abspath = os.path.abspath(os.path.dirname(__file__))
    conf_file = os.path.join(abspath, "tests/conf.py")
    test_file = os.path.join(abspath, "tests/test_demo.py")
    log_dir = "/var/log/cockpit-ovirt-auto"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    result_json = log_dir + "/cockpit-result.json"
    result_html = log_dir + "/cockpit-result.html"

    email_subject = "Test Report For Cockpit-ovirt"
    email_from = "dguo@redhat.com"
    email_to = ["dguo@redhat.com", "ycui@redhat.com", "weiwang@redhat.com"]
    email_text = "Please see the Test Report of Cockpit-ovirt"
    email_attachment = ""

    redis_act = RedisAction()
    while True:
        ipaddr = redis_act.receive_ipaddr()
        if ipaddr == 1:
            print "Break for next test!"
            time.sleep(5)
            continue
        elif ipaddr == 2:
            print "All the test finished!"
            break
        else:
            try:
                while True:
                    print "Try to connect %s" % ipaddr
                    try:
                        redis_act.test_connection(ipaddr)
                    except Exception:
                        time.sleep(10)
                        continue

                    print "Connect succeed! try to run test now..."

                    # Modify the conf.py to add the host ip
                    local("""sed -i 's/HOST_IP =.*/HOST_IP="%s"/' %s""" % (str(ipaddr), str(conf_file)))

                    # Execute to do the tests
                    pytest.main("-s -v %s --json=%s --html=%s" % (test_file, result_json, result_html))

                    # Parse the results and pass to redis
                    res = format_result(result_json)
                    redis_act.publish_result(res)

                    # Send email to administrator
                    email = EmailAction()
                    now = time.strftime("%y-%m-%d-%H-%M-%S")
                    attach_name = log_dir + now + '.' + os.path.basename(result_html)
                    os.rename(result_html, attach_name)
                    email_attachment = [attach_name]
                    email.send_email(
                        email_from,
                        email_to,
                        email_subject,
                        email_text,
                        email_attachment)

                    raise Exception("Done")
            except Exception as e:
                if e != "Done":
                    print e
                break
