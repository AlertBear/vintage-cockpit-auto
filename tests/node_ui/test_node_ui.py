import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.node_status_page import NodeStatusPage
from pages.dashboard_page import DashboardPage
from fabric.api import env


ROOT_URI = "https://10.66.8.217:9090"
env.host_string = 'root@10.66.8.217'
env.password = 'redhat'
test_build = 'rhvh-4.0-0.20160919.0'

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
    node_status_page.check_node_health()


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
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status_fc()


def _test_node_status_efi(firefox):
    """RHEVM-16585"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status_efi()


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


def _test_list_vms(firefox):
    """RHEVM-16600"""
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_vms()


def test_ovirt_dashboard(firefox):
    """RHEVM-16601"""
    dashboard_page = DashboardPage(firefox)
    dashboard_page.basic_check_elements_exists()
