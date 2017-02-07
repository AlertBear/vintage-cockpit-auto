import pytest
from pages.rhel73.he_install import he_install
from fabric.api import env, settings, run
from conf import *

host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD

env.host_string = host_user + '@' + host_ip
env.password = host_password

nfs_ip = NFS_IP
nfs_password = NFS_PASSWORD
nfs_storage_path = NFS_STORAGE_PATH
rhvm_appliance_path = RHVM_APPLIANCE_PATH
nic = NIC
deploy_mode = DEPLOY_MODE
storage_path = STORAGE_PATH
mac = MAC
vm_fqdn = VM_FQDN
vm_ip = VM_IP
vm_password = VM_PASSWORD
engine_password = ENGINE_PASSWORD
auto_answer = AUTO_ANSWER


@pytest.fixture(autouse=True)
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -qa|grep cockpit-ovirt"
        cockpit_ovirt_version = run(cmd)

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append(('redhat-release', redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append(('cockpit-ovirt', cockpit_ovirt_version))


@pytest.fixture(scope="module")
def firefox(request):
    pass


def test_16341(firefox):
    """
    Purpose:
        RHEVM-16341
        Tests the HE_install
    """
    host_dict = {'host_ip': host_ip,
    'host_user': host_user,
    'host_password': host_password}   

    nfs_dict = {
    'nfs_ip': nfs_ip,
    'nfs_password': nfs_password,
    'nfs_path': nfs_storage_path}

    install_dict = {
    'rhvm_appliance_path': rhvm_appliance_path,
    'nic': nic,
    'deploy_mode': deploy_mode,
    'storage_path': storage_path, 
    'mac': mac}

    vm_dict = {
    'vm_fqdn': vm_fqdn,
    'vm_ip': vm_ip,
    'vm_password': vm_password,
    'engine_password': engine_password,
    'auto_answer': auto_answer
    }

    he_install(host_dict, nfs_dict, install_dict, vm_dict)
