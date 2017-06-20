import pytest
from pages.v41.he_install import *
from fabric.api import env, run, settings
from conf import *

host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD

env.host_string = host_user + '@' + host_ip
env.password = host_password

nfs_ip = NFS_IP
nfs_password = NFS_PASSWORD
nfs_storage_path = HE_INSTALL_NFS
rhvm_appliance_path = RHVM_APPLIANCE_PATH
vm_mac = HE_VM_MAC
vm_fqdn = HE_VM_FQDN
vm_ip = HE_VM_IP
vm_password = HE_VM_PASSWORD
engine_password = ENGINE_PASSWORD
auto_answer = AUTO_ANSWER
he_bvnic_mapper = HE_BVNIC_MAPPER


@pytest.fixture(scope="session", autouse=True)
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -qa|grep cockpit-ovirt"
        cockpit_ovirt_version = run(cmd)

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append((
                'redhat-release', redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append((
            'cockpit-ovirt', cockpit_ovirt_version))


@pytest.fixture(scope="module")
def firefox(request):
    pass


def test_18674(firefox):
    """
    Purpose:
        RHEVM-18667
        Setup hosted engine through ova with bond as network
    """
    # Get the nic from he_bvnic_mapper
    if host_ip not in he_bvnic_mapper.keys():
        assert 0, "This system is not configured " \
                  "with a bond or not record in our configuration"
    he_nic = he_bvnic_mapper[host_ip]['BOND_NIC']

    # Test the nic is existing and has an ip address
    cmd = "ip a s|grep %s|grep inet" % he_nic
    with settings(warn_only=True):
        res = run(cmd)
    if res.failed:
        assert 0, "No %s on %s or not configured with ip" % (
            he_nic, host_ip)

    host_dict = {'host_ip': host_ip,
    'host_user': host_user,
    'host_password': host_password}

    nfs_dict = {
    'nfs_ip': nfs_ip,
    'nfs_password': nfs_password,
    'nfs_path': nfs_storage_path}

    install_dict = {
    'rhvm_appliance_path': rhvm_appliance_path,
    'he_nic': he_nic}

    vm_dict = {
    'vm_mac': vm_mac,
    'vm_fqdn': vm_fqdn,
    'vm_ip': vm_ip,
    'vm_password': vm_password,
    'engine_password': engine_password,
    'auto_answer': auto_answer
    }

    he_install(host_dict, nfs_dict, install_dict, vm_dict)

    # Check the hosted engine is deployed
    check_he_is_deployed(host_ip, host_user, host_password)
