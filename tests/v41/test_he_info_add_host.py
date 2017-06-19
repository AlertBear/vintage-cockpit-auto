import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.v41.hosted_engine_page import HePage
from fabric.api import env, run, settings
from utils.helpers import RhevmAction
from conf import *


host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD
another_host = SECOND_HOST
another_password = SECOND_PASSWORD
ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_user + '@' + host_ip
env.password = host_password

vm_fqdn = HE_VM_FQDN
vm_ip = HE_VM_IP
vm_password = HE_VM_PASSWORD
second_nfs_path = HE_DATA_NFS  # Be added to hosted engine
second_host_ip = SECOND_HOST       # Second host to run hosted engine
second_password = SECOND_PASSWORD


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
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()


def test_login(firefox):
    login_page = LoginPage(firefox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def test_18668(firefox):
    """
    RHEVM-18668
        Setup additional host
    """
    '''
    # Add another nfs storage to default DC
    he_rhvm = RhevmAction(vm_fqdn)
    he_rhvm.attach_storage_to_datacenter(second_nfs_path, 'Default')

    # Add another host to default DC where also can be running HE
    he_rhvm.add_new_host(
        second_host_ip,
        "cockpit-he2",
        second_password,
        deploy_hosted_engine=True)
    time.sleep(120)
    '''
    he_page = HePage(firefox)
    he_page.check_additonal_host(vm_fqdn, "cockpit-he2")
    he_page.remove_host_from_rhvm(vm_fqdn, "cockpit-he2")


def test_18678(firefox):
    """
    RHEVM-18678
        Put the host into local maintenance
    """
    # Put the host to local maintenance
    he_page = HePage(firefox)
    he_page.put_host_to_local_maintenance()
    he_page.check_host_in_local_maintenance()


def test_18679(firefox):
    """
    RHEVM-18679
        Remove the host from maintenance
    """
    he_page = HePage(firefox)

    # Check the host is in local maintenance
    he_page.check_host_in_local_maintenance()

    # Remove the host from local maintenance
    he_page.remove_host_from_local_maintenance()

    # Check the host is in local maintenance
    he_page.check_host_not_in_local_maintenance()


def test_18680(firefox):
    """
    RHEVM-18680
        Put the cluster into global maintenance
    """
    he_page = HePage(firefox)

    # Put the cluster into global maintenance
    he_page.put_cluster_to_global_maintenance()

    # Check the cluster is in global maintenance
    he_page.check_cluster_in_global_maintenance()


'''
def test_18681(firefox):
    """
    RHEVM-18681
        Migrate HE
    """
    # To Do
    pass
'''
