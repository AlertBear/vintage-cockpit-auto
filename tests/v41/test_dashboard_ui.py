import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.v41.dashboard_nodestatus_page import NodeStatusPage
from fabric.api import env, run, settings
from conf import *


host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD
test_build = TEST_BUILD
ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_user + '@' + host_ip
env.password = host_password

rhvm_fqdn = RHVM_FQDN


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


'''
def test_18533(firefox):
    """
    RHEVM-18533
        Check the running Virtual Machines quantity in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_virtual_machine()
'''


def test_18534(firefox):
    """
    RHEVM-18534
        Check node status in virtualization dashboard.
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status()


def test_18535(firefox):
    """
    RHEVM-18535
        Check node health in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_health(is_registerd=True)


def test_18536(firefox):
    """
    RHEVM-18536
        Check node health in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_info(test_layer)


'''
def test_18537(firefox):
    """
    RHEVM-18537
        Check node rollback in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_rollback(test_layer)
'''


def test_18540(firefox):
    """
    RHEVM-18540
        Go to the Networking page in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_network_func()


def test_18541(firefox):
    """
    RHEVM-18541
        Go to the Logs page in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_system_log()


def test_18542(firefox):
    """
    RHEVM-18542
        Go to the Storage page in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_storage()


def test_18543(firefox):
    """
    RHEVM-18543
        Check the ssh host key in virtualization dashboard
    """
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_ssh_key()
