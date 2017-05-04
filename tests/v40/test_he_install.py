import pytest
from pages.rhvh40.he_install import he_install
from fabric.api import env
from conf import *


env.host_string = 'root@' + HOST_IP
env.password = HOST_CREDENTIAL[-1]

nfs_ip = yzhao.NFS_IP
nfs_password = yzhao.NFS_PASSWORD
nfs_storage_path = yzhao.NFS_STORAGE_PATH
ova_path = yzhao.OVA_PATH
nic = yzhao.NIC
deploy_mode = yzhao.DEPLOY_MODE
storage_path = yzhao.STORAGE_PATH
mac = yzhao.MAC
vm_fqdn = yzhao.VM_FQDN
vm_ip = yzhao.VM_IP
vm_password = yzhao.VM_IP
engine_password = yzhao.ENGINE_PASSWORD
auto_answer = yzhao.AUTO_ANSWER


@pytest.fixture(scope="module")
def firefox(request):
    pass


def test_16341(firefox):
    """
    Purpose:
        RHEVM-16341
        Tests the HE_install
    """
    host_dict = {'host_ip': HOST_IP,
    'host_user': 'root',
    'host_password': HOST_CREDENTIAL[-1]}   

    nfs_dict = {
    'nfs_ip': nfs_ip,
    'nfs_password': nfs_password,
    'nfs_path': nfs_storage_path}

    install_dict = {
    'ova_path': ova_path,
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
