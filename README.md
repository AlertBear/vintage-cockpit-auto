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
| hp-z620-05.qe.lab.eng.nay.redhat.com | `2c:44:fd:3a:d7:d7`  | 10.66.150.175 | eno1 | RHEL | *YES* |
| hp-z620-04.qe.lab.eng.nay.redhat.com | `2c:44:fd:3a:d7:b6`  | 10.66.148.24 | enp1s0 | CENTOS | *YES* |
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
3. To trigger manually, copy the request.json.example to /tmp/request.json and modify the corresponding value
```bash
#
# test_host: The host where to be test, can be written as ip or hostname
# test_build: The rhvh test build
# test_scenario: The test scenario in the test_scen.py file
#
{
    "test_host": "10.66.148.7",
    "test_build": "redhat-virtualization-host-4.1-20170616.0",
    "test_scenario": "v41_debug_tier"
}
```
4. Run the executable file run.py
```bash
python run.py
```
5. To trigger automatically, please use the [rhvh auto testing platform](http://10.73.73.23/#/cockpit)
