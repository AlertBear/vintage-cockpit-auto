import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh40.node_status_page import NodeStatusPage
from pages.rhvh40.dashboard_page import DashboardPage
from fabric.api import env
from pages.rhvh40.nodectl import Nodectl
from pages.rhvh40.subscriptions_page import SubscriptionsPage
from conf import *


host_ip = HOST_IP
add_hostname = dguo.ADD_HOSTNAME
host_username = HOST_CREDENTIAL[0]
host_password = HOST_CREDENTIAL[1]
test_build = BUILD_VERSION
ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_username + '@' + host_ip
env.password = host_password

rhvm_fqdn = dguo.RHVM_FQDN

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
    login_page.login_with_credential()


def test_16579(firefox):
    """RHEVM-16579"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status()


def test_16580(firefox):
    """RHEVM-16580"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_health(is_registerd=False)
    if not node_status_page.query_host_is_registerd(rhvm_fqdn, add_hostname):
        node_status_page.add_host_to_rhvm(rhvm_fqdn, host_ip, add_hostname, host_password)
    node_status_page.check_node_health(is_registerd=True)


def test_16581(firefox):
    """RHEVM-16581"""
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_info(test_layer)


def test_16582(firefox):
    """RHEVM-16582"""
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + "+1"
    node_status_page.check_node_layer(test_layer)


def test_16583(firefox):
    """RHEVM-16583"""
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_rollback(test_layer)


def test_16588(firefox):
    """RHEVM-16588"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_system_log()


def test_16589(firefox):
    """RHEVM-16589"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_storage()


def test_16590(firefox):
    """RHEVM-16590"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_ssh_key()


def test_16600(firefox):
    """RHEVM-16600"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_list_vms()


def test_16601(firefox):
    """RHEVM-16601"""
    dashboard_page = DashboardPage(firefox)
    dashboard_page.basic_check_elements_exists()


def test_16598(firefox):
    """
    rhsm
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.check_register_rhsm()
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    subscriptions_page.unregister_subsciption()


def test_17034(firefox):
    """
    rhsm_keyOrg
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.check_register_rhsm_key_org()
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    subscriptions_page.unregister_subsciption()


def test_16752(firefox):
    """
    rhsm_satelliate
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.add_domain_name(
        weiwang.SATELLITE_IP,
        weiwang.SATELLITE_HOSTNAME,
        weiwang.HOSTS_FILE)
    # install CA
    subscriptions_page.ca_install(weiwang.CA_PATH)
    subscriptions_page.check_register_satellite()
    subscriptions_page.check_subscription_result()
    subscriptions_page.unregister_subsciption()
    subscriptions_page.reset(weiwang.CA_PATH)


def test_16750(firefox):
    """
    rhsm_password_encrypted_log
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.check_register_rhsm()
    subscriptions_page.check_password_encrypted()
    subscriptions_page.unregister_subsciption()


def test_16591(firefox):
    """
    Purpose:
        RHEVM-16591
        Tets the nodectl help subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_help()


def test_16594(firefox):
    """
    Purpose:
        RHEVM-16594
        Test teh nodectl info subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_info(test_build)


def test_16604(firefox):
    """
    Purpose:
        RHEVM-16604
        Test the nodectl check subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_check()


def test_16605(firefox):
    """
    Purpose:
        RHEVM-16605
        Test the nodectl sub-command --debug
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_debug()


def test_16606(firefox):
    """
    Purpose:
        RHEVM-16606
        Test the nodectl sub-command --machine-readable
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_json()
