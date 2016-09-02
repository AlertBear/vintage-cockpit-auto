import pytest
from selenium import webdriver
from pages.login_page import LoginPage
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


def test_rhsm_page(firfox):
    subscriptions_page = SubscriptionsPage(firfox)
    subscriptions_page.basic_check_elements_exists()
    subscriptions_page.register_rhsm()
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    # subscriptions_page.unregister_subsciption()


# def test_rhsm_keyOrg_page(firfox):
#     subscriptions_page = SubscriptionsPage(firfox)
#     subscriptions_page.basic_check_elements_exists()
#     subscriptions_page.register_rhsm_key_org()
#     subscriptions_page.check_subscription_result()
#     # subscriptions_page.unregister_subsciption()
