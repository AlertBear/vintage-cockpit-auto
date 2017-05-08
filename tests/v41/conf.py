#
# The variable to be used by each case
#
TEST_BUILD = "redhat-virtualization-host-4.1-20170421.0"
HOST_IP = "10.66.148.7"
HOST_USER = "root"
HOST_PASSWORD = "redhat"


#
# Config variable to be used by adding host to engine
#
RHVM_FQDN = "rhvm41-vdsm-auto.lab.eng.pek2.redhat.com"


#
# Config variable to be used by Subscription cases
#
RHN_USER = "qa@redhat.com"
RHN_PASSWORD = "CZvGMy7TwJpVKW9t"
ACTIVATION_KEY = "rhevh"
ACTIVATION_ORG = "711497"
SATELLITE_IP = "10.73.75.61"
SATELLITE_HOSTNAME = "satellite62.lab.eng.pek2.redhat.com"
SATELLITE_USER = "admin"
SATELLITE_PASSWORD = "redhat"
CA_PATH = "https://10.73.75.61/pub/katello-ca-consumer-satellite62.lab.eng.pek2.redhat.com-1.0-1.noarch.rpm"


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
SECOND_HOST = "10.66.9.52"
SECOND_PASSWORD = "redhat"
SECOND_VM_FQDN = "cockpit-vm"
HE_BVNIC_MAPPER = {
    "10.66.148.7": {
        # Bond/VLAN/BV is identical with the network
        # configured during ks installation
        "HOSTNAME": "dell-op790-01.lab.eng.pek2.redhat.com",
        "BOND_NIC": "bond0",
        "VLAN_NIC": "p3p1.20",
        "BV_NIC": "bond0.20"},

    "10.73.75.x": {
        # Bond/VLAN/BV is identical with the network
        # configured during ks installation
        "HOSTNAME": "dell-per510-01.lab.eng.pek2.redhat.com",
        "BOND_NIC": "bond0",
        "VLAN_NIC": "p3p2.50",
        "BV_NIC": "bond0.50"}
}
