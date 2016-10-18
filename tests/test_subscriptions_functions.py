import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.subscriptions_page import SubscriptionsPage
from conf import *

ROOT_URI = "https://" + HOST_IP + ":9090"

@pytest.fixture(scope="module")
def firfox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()


def test_login(firfox):
    login_page = LoginPage(firfox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential()


def test_16598(firfox):
    """
    rhsm
    """
    subscriptions_page = SubscriptionsPage(firfox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.register_rhsm()
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    subscriptions_page.unregister_subsciption()


def test_17034(firfox):
    """
    rhsm_keyOrg
    """
    subscriptions_page = SubscriptionsPage(firfox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.register_rhsm_key_org()
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    subscriptions_page.unregister_subsciption()


def test_16752(firfox):
    """
    rhsm_satelliate
    """
    subscriptions_page = SubscriptionsPage(firfox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.add_domain_name()
    # install CA
    subscriptions_page.ca_install()
    subscriptions_page.register_satellite()
    subscriptions_page.check_subscription_result()
    subscriptions_page.unregister_subsciption()
    subscriptions_page.reset()


def test_16750(firfox):
    """
    rhsm_password_encrypted_log
    """
    subscriptions_page = SubscriptionsPage(firfox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.register_rhsm()
    subscriptions_page.check_password_encrypted()
    subscriptions_page.unregister_subsciption()
