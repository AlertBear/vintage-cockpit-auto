import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.node_status_page import NodeStatusPage
from pages.dashboard_page import DashboardPage
from fabric.api import env
from utils.helpers import Config


cfg = Config('./cockpit.ini')

host_ip = cfg.get('SHARE', 'HOST_IP')
host_user = cfg.get('SHARE', 'HOST_USER')
host_password = cfg.get('SHARE', 'HOST_PASSWORD')
test_build = cfg.get('SHARE', 'TEST_BUILD')
ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_user +'@' + host_ip
env.password = host_password

add_hostname = cfg.get('DB', 'ADD_HOSTNAME')
rhvm_fqdn = cfg.get('DB', 'RHVM_FQDN')

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


def _test_16578(firefox):
    """RHEVM-16578"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_virtual_machine()


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


def _test_16584(firefox):
    """RHEVM-16584"""
    # This will be tested on a rhvh with FC
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_status_fc(test_layer)


def _test_16585(firefox):
    """RHEVM-16585"""
    # This will be tested on a rhvh with EFI
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_status_efi(test_layer)


def _test_16586(firefox):
    """RHEVM-16586"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_rollabck_func()


def _test_16587(firefox):
    """RHEVM-16587"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_network_func()


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
