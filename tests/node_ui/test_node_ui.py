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


def test_node_status(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status()


def test_node_health(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_health()

"""
def test_node_info(firefox):
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_info(test_layer)


def test_node_rollback(firefox):
    node_status_page = NodeStatusPage(firefox)
    test_layer = test_build + '+1'
    node_status_page.check_node_rollback(test_layer)


def test_node_status_fc(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status_fc()


def test_node_status_efi(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_status_efi()


def test_system_log(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_system_log()


def test_storage(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_storage()


def test_ssh_key(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_ssh_key()
"""


def test_ovirt_dashboard(firefox):
    dashboard_page = DashboardPage(firefox)
    dashboard_page.basic_check_elements_exists()
