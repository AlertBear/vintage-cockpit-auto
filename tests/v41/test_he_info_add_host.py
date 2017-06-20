import pytest
import time
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

he_vm_fqdn = HE_VM_FQDN
he_vm_ip = HE_VM_IP
he_vm_password = HE_VM_PASSWORD
he_rhvm = RhevmAction(he_vm_fqdn, "admin", "password")

sd_name = "heauto-sd"
storage_type = "nfs"
storage_addr = NFS_IP
storage_pass = NFS_PASSWORD
storage_path = HE_DATA_NFS

second_host_ip = SECOND_HOST       # Second host to run hosted engine
second_password = SECOND_PASSWORD


def check_sd_is_attached(sd_name):
    if he_rhvm.list_storage_domain(sd_name):
        return True

if not check_sd_is_attached(sd_name):
    with settings(warn_only=True):
        host_name = run("hostname")

    # Clean the nfs path
    cmd = "rm -rf %s/*" % storage_path
    with settings(
        warn_only=True,
        host_string='root@' + storage_addr,
        password=storage_pass):
        run(cmd)

    # Add nfs storage to Default DC on Hosted Engine,
    # which is used for creating vm
    he_rhvm.create_plain_storage_domain(
        sd_name=sd_name,
        sd_type='data',
        storage_type=storage_type,
        storage_addr=storage_addr,
        storage_path=storage_path,
        host=host_name)

    he_rhvm.attach_sd_to_datacenter(sd_name=sd_name, dc_name='Default')


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
    # Add another host to default DC where also can be running HE
    second_host_name = "cockpit-he2"
    he_rhvm.create_new_host(
        ip=second_host_ip,
        host_name=second_host_name,
        password=second_password,
        cluster_name='Default',
        deploy_hosted_engine=True)
    time.sleep(60)

    i = 0
    while True:
        if i > 60:
            assert 0, "Timeout waitting for host is up"
        host_status = he_rhvm.list_host(second_host_name)['status']
        if host_status == 'up':
            break
        elif host_status == 'install_failed':
            assert 0, "Host is not up as current status is: %s" % host_status
        elif host_status == 'non_operational':
            assert 0, "Host is not up as current status is: %s" % host_status
        time.sleep(10)
        i += 1


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
