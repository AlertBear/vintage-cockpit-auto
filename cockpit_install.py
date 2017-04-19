#!/usr/bin/python2.7

import sys
import re
import time
import json
from fabric.api import run, settings

# Since RHEL/Fedora/Centos is already installed on specified system,
# list the corresponding ip
sys_ip_mapper = {
    "hp-z620-05.qe.lab.eng.nay.redhat.com": "10.66.x.x",
    "dell-pet105-02.qe.lab.eng.nay.redhat.com": "10.66.x.x",
    "hp-z620-04.qe.lab.eng.nay.redhat.com": "10.66.x.x",
    "bootp-73-75-177.lab.eng.pek2.redhat.com": "10.73.75.177"
}


if __name__ == "__main__":
    # The first argv is test system which will be used
    sys_install = sys.argv[1]
    # The remaining argv are test scenarios
    scens_test = []
    for i in range(2, len(sys.argv)):
        scens_test.append(sys.argv[i])

    # Get the machine and parse to /tmp/http.json
    if sys_install in sys_ip_mapper:
        host_ip = sys_ip_mapper[sys_install]
    else:
        raise Exception("No such machine with existing SYS installed")

    # Get the version of cockpit from test scenario
    if re.search("v41", sys.argv[2]):
        cockpit_ovirt_ver = "4.1"
        cockpit_ovirt_ver_simp = "41"
    elif re.search("v40", sys.argv[2]):
        cockpit_ovirt_ver = "4.0"
        cockpit_ovirt_ver_simp = "40"

    if re.search("rhel", sys.argv[2]):
        rpm_repo_url = "http://bob.eng.lab.tlv.redhat.com/builds" \
            "/latest_{}/rhv-release-latest-{}.noarch.rpm".format(
                cockpit_ovirt_ver, cockpit_ovirt_ver)
    else:
        rpm_repo_url = "http://resources.ovirt.org/pub/yum-repo/" \
            "ovirt-release{}.rpm".format(cockpit_ovirt_ver_simp)

    # Delete the old cockpit and cockpit-ovirt-dashboard
    with settings(
        warn_only=True,
        host_string="root@"+host_ip,
        password="redhat"
    ):
        # Delete the old repo rpm
        cmd = "rpm -qa|grep rhv-release"
        output = run(cmd)
        cmd = "rpm -e %s" % output
        run(cmd)

        # Delete the old cockpit and cockpit-ovirt-dashboard
        cmd = "yum erase -y cockpit*"
        run(cmd)
        cmd = "yum erase -y cockpit-ovirt-dashboard"
        run(cmd)

    # Install the latest cockpit and cockpit-ovirt-dashboard
    with settings(
        host_string="root@"+host_ip,
        password="redhat"
    ):
        cmd = "yum install -y %s" % rpm_repo_url
        run(cmd)
        time.sleep(10)

        cmd = "yum install -y cockpit"
        run(cmd)
        cmd = "yum install -y cockpit-ovirt-dashboard"
        run(cmd)

        # Enable cockpit and open firewall
        cmd = "systemctl enable --now cockpit.socket"
        run(cmd)
        cmd = "firewall-cmd --add-service=cockpit"
        run(cmd)
        cmd = "firewall-cmd --add-service=cockpit --permanent"
        run(cmd)

    # Create /tmp/http.json for run.py
    http_dict = {
        "test_profile": scens_test,
        "host_ip": host_ip,
        "test_build": ""
    }
    with open("/tmp/http.json", 'w') as f:
        json.dump(http_dict, f, indent=2)
