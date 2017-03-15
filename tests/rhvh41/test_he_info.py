import time
import pytest
import re
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh41.hosted_engine_page import HePage
from fabric.api import env, run, settings
from utils.helpers import RhevmAction
from conf import *


host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD
ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_user + '@' + host_ip
env.password = host_password

vm_fqdn = HE_VM_FQDN
vm_ip = HE_VM_IP
vm_password = HE_VM_PASSWORD
engine_password = ENGINE_PASSWORD
he_data_nfs = HE_DATA_NFS



@pytest.fixture(autouse=True)
def _environment(request):
    cmd_imgbase = "imgbase w"
    output_imgbase = run(cmd_imgbase)
    rhvh_version = output_imgbase.split()[-1].split('+')[0]
    request.config._environment.append(('rhvh-version', rhvh_version))

    cmd = "rpm -qa|grep cockpit-ovirt"
    cockpit_ovirt_version = run(cmd)
    request.config._environment.append(('cockpit-ovirt', cockpit_ovirt_version))


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


def test_18669(firefox):
    """
    RHEVM-18669
        Hosted Engine status can be checked after configuration
    """
    he_page = HePage(firefox)
    he_page.check_engine_status()


def test_18670(firefox):
    """
    RHEVM-18670
        Check the vm still up after reboot node
    """
    # To do: Reboot RHVH
    pass

    he_page = HePage(firefox)

    # Check engine status
    he_page.check_engine_status()

    # Check VM state
    he_page.check_vm_status()


def test_18671(firefox):
    """
    RHEVM-18671
        Reboot RHVH after finished configure hosted engine
    """
    # To do: Reboot RHVH
    pass

    he_page = HePage(firefox)

    # Check engine status
    he_page.check_engine_status()
    time.sleep(2)

    # Check three maintenance buttons exist
    he_page.check_three_buttons()


def test_18672(firefox):
    """
    RHEVM-18672
        Verify hosted-engine cockpit show correct info after setup hosted engine with OVA
    """
    he_page = HePage(firefox)

    # Check engine status
    he_page.check_engine_status()

    # Check three maintenance buttons exist
    he_page.check_he_running_on_host(host_ip)

    # Check vm statues
    he_page.check_vm_status()


'''
def test_18684(firefox):
    """
    RHEVM-18684
        Check if there are a large number of redundant log generation in /var/log/messages
    """
    # To Do
    pass
'''


def test_18685(firefox):
    """
    RHEVM-18685
        Check there is no Hosted Engine passwords are saved in the logs as clear text
    """
    # Find the hosted engine setup log
    cmd = "find /var/log -type f |grep ovirt-hosted-engine-setup-.*.log"
    output_log = run(cmd)

    # Find the line contains "Enter engine admin password"
    cmd = "grep 'Enter engine admin password' %s" % output_log
    with settings(warn_only=True):
        output_password = run(cmd)

    assert not re.search(engine_password, output_password),     \
        "Hosted engine password is saved in the logs as clear text"


def test_he_create_vm(firefox):
    """
    Purpose:
        Create a vm under HE host, which for tests/rhvh41/test_vm_resgisterd.py
    """
    # Add nfs storage to Default DC on Hosted Engine,
    # which is used for creating vm
    he_rhvm = RhevmAction(he_vm_fqdn)
    he_rhvm.attach_storage_to_datacenter(he_data_nfs, 'Default')

    # Create new vm without installing guest os under Default DC
    he_rhvm.add_new_host(
        second_host_ip,
        "cockpit-he2",
        second_password,
        deploy_hosted_engine=True)
    time.sleep(120)
