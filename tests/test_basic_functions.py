import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.subscriptions_page import SubscriptionsPage
from pages.node_status_page import NodeStatusPage


ROOT_URI = "https://10.66.11.209:9090"


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


def test_main_page(firefox):
    main_page = MainPage(firefox)
    main_page.basic_check_elements_exists()


def test_subscriptions_page(firefox):
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.register_to_rhsm()


def test_node_status_page(firefox):
    node_status_page = NodeStatusPage(firefox)
    node_status_page.basic_check_elements_exists()
