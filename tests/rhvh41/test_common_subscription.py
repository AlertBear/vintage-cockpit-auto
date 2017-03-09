import pytest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh41.subscriptions_page import SubscriptionsPage
from fabric.api import env, run
from conf import *


host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD

ca_path = CA_PATH
activation_key = ACTIVATION_KEY
activation_org = ACTIVATION_ORG
rhn_user = RHN_USER
rhn_password = RHN_PASSWORD
satellite_ip = SATELLITE_IP
satellite_hostname = SATELLITE_HOSTNAME
satellite_user = SATELLITE_USER
satellite_password = SATELLITE_PASSWORD

ROOT_URI = "https://" + host_ip + ":9090"
env.host_string = host_user + '@' + host_ip
env.password = host_password


@pytest.fixture(autouse=True)
def _environment(request):
    cmd = "rpm -qa|grep cockpit-ovirt"
    cockpit_ovirt_version = run(cmd)

    cmd = "rpm -q imgbased"
    result = run(cmd)
    if result.failed:
        cmd = "cat /etc/redhat-release"
        redhat_release = run(cmd)
        request.config._environment.append(('redhat-release', redhat_release))
    else:
        cmd_imgbase = "imgbase w"
        output_imgbase = run(cmd_imgbase)
        rhvh_version = output_imgbase.split()[-1].split('+')[0]
        request.config._environment.append(('rhvh-version', rhvh_version))

    request.config._environment.append(('cockpit-ovirt', cockpit_ovirt_version))


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
    login_page.login_with_credential(host_user, host_password)


def test_18412(firefox):
    """
    RHEVM-18412
        Subscription to RHSM
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.check_register_rhsm(rhn_user, rhn_password)
    time.sleep(5)
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    subscriptions_page.unregister_subsciption()


def test_18413(firefox):
    """
    RHEVM-18413
        Subscription to RHSM with key and organization
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.check_register_rhsm_key_org(
        activation_key,
        activation_org)
    time.sleep(5)
    subscriptions_page.check_subscription_result()
    # TODO: need to verify RHN sit
    subscriptions_page.unregister_subsciption()


def test_18414(firefox):
    """
    RHEVM-18414
        Check password is encrypted in log after Subscription to RHSM
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.check_register_rhsm(rhn_user, rhn_password)
    subscriptions_page.check_password_encrypted(rhn_password)
    subscriptions_page.unregister_subsciption()


'''
def test_18415(firefox):
    """
    RHEVM-18415
        Subscription to Satellite server
    """
    subscriptions_page = SubscriptionsPage(firefox)
    subscriptions_page.add_domain_name(
        satellite_ip,
        satellite_hostname)
    # install CA
    subscriptions_page.ca_install(ca_path)
    subscriptions_page.check_register_satellite(
        satellite_ip,
        satellite_user,
        satellite_password)
    subscriptions_page.check_subscription_result()
    subscriptions_page.unregister_subsciption()
    subscriptions_page.reset(ca_path)
'''
