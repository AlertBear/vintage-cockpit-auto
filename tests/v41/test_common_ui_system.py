import pytest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from pages.v41.ui_system_page import SystemPage
from fabric.api import env, run
from conf import *


host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD
second_ip = SECOND_HOST
second_password = SECOND_PASSWORD

ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_user + '@' + host_ip
env.password = host_password


@pytest.fixture(autouse=True)
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -qa|grep cockpit-ovirt"
        cockpit_ovirt_version = run(cmd)

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append((
                'redhat-release', redhat_release))
        else:
            cmd_imgbase = "imgbase w"
            output_imgbase = run(cmd_imgbase)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append(('rhvh-version', rhvh_version))

        request.config._environment.append((
            'cockpit-ovirt', cockpit_ovirt_version))


@pytest.fixture(scope="module")
def firefox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()


def test_18379(firefox):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is default in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknow_default()


def test_18381(firefox):
    """
    RHEVM-18379
        Wrong account to login into remote machine
        with "allowUnknow" is true in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknown_true_wrong_account(second_ip)


def test_18382(firefox):
    """
    RHEVM-18382
        Login remote closed host with "allowUnknow" is true in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknown_true_remote_closed(
        second_ip,
        "root",
        second_password)


def test_18383(firefox):
    """
    RHEVM-18383
        Login remote host with wrong address in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknown_true_wrong_address()


def test_18384(firefox):
    """
    RHEVM-18384
        Login remote host with wrong address in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknown_true_empty_username(
        second_ip,
        "root",
        second_password)


def test_18380(firefox):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is true in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknown_true(
        second_ip,
        "root",
        second_password)


def test_18377(firefox):
    """
    RHEVM-18377
        Login cockpit via Firefox browser
    """
    login_page = LoginPage(firefox)
    login_page.basic_check_elements_exists()
    login_page.login_with_incorrect_credential()
    time.sleep(2)
    login_page.login_with_credential(host_user, host_password)
    system_page = SystemPage(firefox)
    system_page.check_login_host(host_ip)


def test_18385(firefox):
    """
    RHEVM-18385
        Configure hostname
    """
    system_page = SystemPage(firefox)
    system_page.configure_hostname()
    system_page.check_configure_hostname()


def test_18386(firefox):
    """
    RHEVM-18386
        Configure timezone
    """
    system_page = SystemPage(firefox)
    system_page.configure_timezone()
    system_page.check_configure_timezone()


def test_18387(firefox):
    """
    RHEVM-18386
        Configure time manually
    """
    system_page = SystemPage(firefox)
    system_page.configure_time()
    system_page.check_configure_time()


def test_18390(firefox):
    """
    RHEVM-18386
        Change performance profile
    """
    system_page = SystemPage(firefox)
    system_page.change_performance_profile()
    system_page.check_change_performance_profile()
