# cockpit-auto

[![build status](http://10.8.176.174/dguo/cockpit-auto/badges/dev/build.svg)](http://10.8.176.174/dguo/cockpit-auto/commits/dev)

## Binded Mac, IP, Hostname For HE Automation

| Hostname | Mac Addr | IP Addr | valid? |
| -------- | -------- | ------- | ------ |
| rhevh-hostedengine-vm-01.qe.lab.eng.nay.redhat.com | 52:54:00:05:61:f2  | 10.66.148.102 | *YES* |
| rhevh-hostedengine-vm-02.qe.lab.eng.nay.redhat.com | 52:54:00:71:d5:ff  | 10.66.148.103 | *YES* |
| rhevh-hostedengine-vm-03.qe.lab.eng.nay.redhat.com | 52:54:00:57:ef:59  | 10.66.148.104 | *YES* |
| rhevh-hostedengine-vm-04.lab.eng.pek2.redhat.com | 52:54:00:5e:8e:c7  | 10.73.73.100 | *YES* |
| rhevh-hostedengine-vm-05.lab.eng.pek2.redhat.com | 52:54:00:5d:21:64  | 10.73.73.101 | *YES* |
| rhevh-hostedengine-vm-06.lab.eng.pek2.redhat.com | 52:54:00:34:04:b0  | 10.73.73.102 | *YES* |

# Test machines used
| Hostname | Mac Addr | IP Addr | NIC | PURPOSE | valid?|
| -------- | -------- | ------- | ------ | ------ | ------ |
| dell-op790-01.qe.lab.eng.nay.redhat.com | `d4:be:d9:95:61:ca`  | 10.66.148.7 | em1 | RHVH BOND VLAN | *YES* |
| hp-z620-05.qe.lab.eng.nay.redhat.com | `2c:44:fd:3a:d7:d7`  | 10.66.149.62 | eno1 | RHEL | *YES* |
| hp-z620-04.qe.lab.eng.nay.redhat.com | `2c:44:fd:3a:d7:b6`  | 10.66.148.24 | enp1s0 | CENTOS | *YES* |
| hp-z620-02.qe.lab.eng.nay.redhat.com | `64:31:50:19:b9:70`  | 10.66.148.22 | enp1s0 | FEDORA | *NO* |
| dell-per510-01.lab.eng.pek2.redhat.com |   |  |  | BOND VLAN FC | *NO* |
| dell-pet105-02.qe.lab.eng.nay.redhat.com | `00:22:19:2d:4b:a3`  | 10.66.148.10 | enp2s0 | TEST RUN | *YES* |


## How To Run

1. Clone source codes to local directory on above "TEST RUN" machine
```bash
git clone http://dguo@10.8.176.174/dguo/cockpit-auto.git
```
2. Install the dependency packages
```bash
pip install -r requirements
```
3. Make a log directory under projects path
```bash
cd cockpit-auto
mkdir logs
```
4. Start a HTTP service under log directory to show admins all the reports created during testing
```bash
python -m SimpleHTTPServer
```
5. Trigger cockpit test manually from [Auto testing platform](http://10.73.73.23/#/cockpit)
