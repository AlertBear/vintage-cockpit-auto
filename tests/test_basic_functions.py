import time
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.subscriptions_page import SubscriptionsPage


ROOT_URI = "https://10.66.11.209:9090"


@pytest.fixture(scope="module")
def firfox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()


def test_login_page(firfox):
    login_page = LoginPage(firfox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential()


def test_main_page(firfox):
    main_page = MainPage(firfox)
    main_page.basic_check_elements_exists()


def test_subscriptions_page(firfox):
    subscriptions_page = SubscriptionsPage(firfox)
    subscriptions_page.basic_check_elements_exists()
    need_test = ["register_rhsm", "register_rhsm_key_org",
        "register_satellite"]
    for item in need_test:
        eval("subscriptions_page." + item + "()")
        subscriptions_page.check_subscription_result()
        subscriptions_page.unregister_subsciption()
