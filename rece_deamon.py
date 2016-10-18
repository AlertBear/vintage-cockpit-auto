#!/usr/bin/python2.7
import redis
import os
import time
import json
import pytest
from fabric import run, local, settings


class RedisAction(object):
    def __init__(self):
        self.redis_host = "10.66.9.216"
        self.redis_conn = redis.StrictRedis(host=self.redis_host, port=6379, db=0, password="redhat")
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
        except Exception:
            return 1

    def test_connection(self, ipaddr):
        with settings(host_string='root@' + ipaddr):
            run("hostname")

    def publish_result(self, data):
        self.redis_conn.publish("dell-per510-01.lab.eng.pek2.redhat.com-cockpit-result", data)


if __name__ == "__main__":
    redis_act = RedisAction()
    while True:
        ipaddr = redis_act.receive_ipaddr()
        if ipaddr == 1:
            print "break for next test!"
            time.sleep(5)
            continue
        elif ipaddr == 2:
            print "all the test finished!"
            break
        else:
            while True:
                print "Try to connect %s" % ipaddr
                try:
                    redis_act.test_connection(ipaddr)
                except Exception:
                    time.sleep(10)
                    continue

                print "Connect succeed! try to run test now..."

                abspath = os.path.abspath(os.path.dirname(__file__))
                conf_file = os.path.join(abspath, "tests/conf.py")
                test_file = os.path.join(abspath, "tests/test_nodectl.py")

                # Modify the conf.py to add the host ip
                local("sed -i 's/HOST_IP =.*/HOST_IP=%s/' %s" % (str(ipaddr), str(conf_file)))

                # Execute to do the tests
                try:
                    pytest.main("-s -v %s --json=result.json")
                except Exception as e:
                    print e
                    break

                # Parse the result and pass to redis channel
                with open('./result.json') as f:
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

                redis_act.publish_result(format_ret)
