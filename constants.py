#
# The variable to be used by each case
#
HOST_USER = "root"
HOST_PASSWORD = "redhat"


#
# Config variable to be used by adding host to engine
#
RHVM_FQDN = "rhvm41-vdsm-auto.lab.eng.pek2.redhat.com"


#
# Config variable to be used by Subscription cases
#
RHN_USER = "QualityAssurance"
RHN_PASSWORD = "VHVFhPS5TEG8dud9"
ACTIVATION_KEY = "rhevh"
ACTIVATION_ORG = "711497"
SATELLITE_IP = "10.73.75.177"
SATELLITE_HOSTNAME = "satellite62.lab.eng.pek2.redhat.com"
SATELLITE_USER = "admin"
SATELLITE_PASSWORD = "redhat"
CA_PATH = "https://10.73.75.177/pub/katello-ca-consumer-satellite62.lab.eng.pek2.redhat.com-1.0-1.noarch.rpm"


#
# Config variable to be used by Hosted Engine cases
#
RHVM_APPLIANCE_PATH = "http://10.66.10.22:8090/rhevm-appliance/"
NFS_IP = "10.66.8.173"
NFS_PASSWORD = "l1admin"
HE_INSTALL_NFS = "/home/dguo/Public/cockpit/he_install"
HE_DATA_NFS = "/home/dguo/Public/cockpit/he_data"
HE_VM_MAC = "52:54:00:05:61:f2"
HE_VM_FQDN = "rhevh-hostedengine-vm-01.qe.lab.eng.nay.redhat.com"
HE_VM_IP = "10.66.148.102"
HE_VM_PASSWORD = "redhat"
ENGINE_PASSWORD = "password"
AUTO_ANSWER = "http://10.73.73.23:8000/run?download=true"
SECOND_HOST = "10.66.148.22"
SECOND_PASSWORD = "redhat"
SECOND_VM_FQDN = "cockpit-vm"


#
# The machine and the corresponding ip
#
SYS_IP_MAP = {
    "hp-z620-05.qe.lab.eng.nay.redhat.com": "10.66.150.175",
    "hp-z620-04.qe.lab.eng.nay.redhat.com": "10.66.148.24",
    "dell-op790-01.qe.lab.eng.nay.redhat.com": "10.66.148.7",
    "dell-pet105-02.qe.lab.eng.nay.redhat.com": "10.66.148.10"
}


#
# Hosted Engine info mapper
#
HE_VM_MAP = {
    "10.66": [
        ("rhevh-hostedengine-vm-01.qe.lab.eng.nay.redhat.com", "52:54:00:05:61:f2", "10.66.148.102"),
        ("rhevh-hostedengine-vm-02.qe.lab.eng.nay.redhat.com", "52:54:00:71:d5:ff", "10.66.148.103"),
        ("rhevh-hostedengine-vm-03.qe.lab.eng.nay.redhat.com", "52:54:00:57:ef:59", "10.66.148.104")],
    "10.73": [
        ("rhevh-hostedengine-vm-04.lab.eng.pek2.redhat.com", "52:54:00:5e:8e:c7", "10.73.73.100"),
        ("rhevh-hostedengine-vm-05.lab.eng.pek2.redhat.com", "52:54:00:5d:21:64", "10.73.73.101"),
        ("rhevh-hostedengine-vm-06.lab.eng.pek2.redhat.com", "52:54:00:34:04:b0", "10.73.73.102")]
}
