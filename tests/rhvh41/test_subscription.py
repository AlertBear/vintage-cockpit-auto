import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.subscriptions_page import SubscriptionsPage
from fabric.api import env
from utils.helpers import Config

cfg = Config('./cockpit.ini')

host_ip = cfg.get('SHARE', 'HOST_IP')
host_user = cfg.get('SHARE', 'HOST_USER')
host_password = cfg.get('SHARE', 'HOST_PASSWORD')

ROOT_URI = "https://" + host_ip + ":9090"
env.host_string = host_user + '@' + host_ip
env.password = host_password

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
