
#
# The variable to be used by each case
#
HOST_IP = "10.66.148.7"
HOST_USER = "root"
HOST_PASSWORD = "redhat"
TEST_BUILD = "rhvh-4.1-0.20170120.0"
REDIS_HOST = "10.66.11.155"

#
# Config variable to be used by test_dashboard_ui.py/
# test_dashboard_ui_efi.py/test_dashboard_ui_fc.py
#
RHVM_FQDN = "rhvm41-vlan50-1.lab.eng.pek2.redhat.com"
ADD_HOSTNAME = "cockpit-ovirt"

#
# Additional Config variable to be used by test_dashboard_ui_fc.py
#
FC_HOST_IP = "10.66.148.7"
FC_HOST_USER = "root"
FC_HOST_PASSWORD = "redhat"

#
# Additional Config variable to be used by test_dashboard_ui_efi.py
#
EFI_HOST_IP = "10.66.148.7"
EFI_HOST_USER = "root"
EFI_HOST_PASSWORD = "redhat"


#
# Config variable to be used by test_common_subscription.py
#
RHN_USER = "qa@redhat.com"
RHN_PASSWORD = "EC3YWpKxSe524GCK"
ACTIVATION_KEY = "rhevh"
ACTIVATION_ORG = "711497"
SATELLITE_IP = "10.73.75.61"
SATELLITE_HOSTNAME = "satellite62.lab.eng.pek2.redhat.com"
SATELLITE_USER = "admin"
SATELLITE_PASSWORD = "redhat"
CA_PATH = "https://10.73.75.61/pub/katello-ca-consumer-satellite62.lab.eng.pek2.redhat.com-1.0-1.noarch.rpm"


#
# Config variable to be used by test_he_install.py/test_he_install_bond.py/
# test_he_install_vlan.py/test_he_install_bv.py
#
RHVM_APPLIANCE_PATH="/home/dguo/Work/iso/rhvm-appliance-4.1.20170126.0-1.el7ev.noarch.rpm"
NFS_IP = "10.66.8.173"
NFS_PASSWORD = "l1admin"
NFS_STORAGE_PATH = "/home/dguo/Public/he"
NIC = "em1"
MAC = "52:54:00:05:61:f2"
VM_FQDN = "rhevh-hostedengine-vm-01.qe.lab.eng.nay.redhat.com"
VM_IP = "10.66.148.102"
VM_PASSWORD = "redhat"
ENGINE_PASSWORD = "password"
AUTO_ANSWER = "/home/dguo/Public/work/run"
SECOND_HOST = "10.66.8.140"
SECOND_PASSWORD = "redhat"


#
# Additional config variable to be used by test_he_install_bond.py
#
BOND_HOST_IP = "10.66.148.7"
BOND_HOST_USER = "root"
BOND_HOST_PASSWORD = "redhat"
BOND_NIC = "bond0"


#
# Additional config variable to be used by test_he_install_vlan.py
#
VLAN_HOST_IP = "10.66.148.7"
VLAN_HOST_USER = "root"
VLAN_HOST_PASSWORD = "redhat"
VLAN_NIC = "em1.50"


#
# Additional config variable to be used by test_he_install_bv.py
#
BV_HOST_IP = "10.66.148.7"
BV_HOST_USER = "root"
BV_HOST_PASSWORD = "redhat"
BV_NIC = "bond0.50"
