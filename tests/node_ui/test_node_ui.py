import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.node_status_page import NodeStatusPage


ROOT_URI = "https://10.66.8.217:9090"


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

"""
def test_node_health(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.basic_check_elements_exists()
    node_status_page.check_node_health()


def test_node_info(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_info()
"""


def test_node_rollback(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.check_node_rollback()
