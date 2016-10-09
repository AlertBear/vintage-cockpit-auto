import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.node_status_page import NodeStatusPage
from pages.dashboard_page import DashboardPage
from fabric.api import env


ROOT_URI = "https://10.66.8.217:9090"
host_ip = "10.66.8.217"
host_name = "cockpit-auto"
host_password = 'redhat'
test_build = 'rhvh-4.0-0.20160928.0'

env.host_string = 'root@' + host_ip
env.password = host_password

rhvm_fqdn = "rhevm-40-1.englab.nay.redhat.com"

@pytest.fixture(scope="module")
def firefox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()


def test_login_page(firefox):
    login_page = LoginPage(firefox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential()


def _test_virtual_machines(firefox):
    """RHEVM-16578"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_virtual_machine()


def test_node_status(firefox):
    """RHEVM-16579"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status()


def test_node_health(firefox):
    """RHEVM-16580"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_health(is_registerd=False)
    if not node_status_page.query_host_is_registerd(rhvm_fqdn, host_name):
        node_status_page.add_host_to_rhvm(rhvm_fqdn, host_ip, host_name, host_password)
    node_status_page.check_node_health(is_registerd=True)


def test_node_info(firefox):
    """RHEVM-16581"""
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_info(test_layer)


def test_node_layers(firefox):
    """RHEVM-16582"""
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + "+1"
    node_status_page.check_node_layer(test_layer)


def test_node_rollback(firefox):
    """RHEVM-16583"""
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_rollback(test_layer)


def _test_node_status_fc(firefox):
    """RHEVM-16584"""
    # This will be tested on a rhvh with FC
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_status_fc(test_layer)


def _test_node_status_efi(firefox):
    """RHEVM-16585"""
    # This will be tested on a rhvh with EFI
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_status_efi(test_layer)


def _test_rollback_func(firefox):
    """RHEVM-16586"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_rollabck_func()


def _test_network_func(firefox):
    """RHEVM-16587"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_network_func()


def test_system_log(firefox):
    """RHEVM-16588"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_system_log()


def test_storage(firefox):
    """RHEVM-16589"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_storage()


def test_ssh_key(firefox):
    """RHEVM-16590"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_ssh_key()


def test_list_vms(firefox):
    """RHEVM-16600"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_list_vms()


def test_ovirt_dashboard(firefox):
    """RHEVM-16601"""
    dashboard_page = DashboardPage(firefox)
    dashboard_page.basic_check_elements_exists()
