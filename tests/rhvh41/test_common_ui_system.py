import pytest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh41.main_page import MainPage
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
    cmd_imgbase = "imgbase w"
    output_imgbase = run(cmd_imgbase)
    rhvh_version = output_imgbase.split()[-1].split('+')[0]
    request.config._environment.append(('rhvh-version', rhvh_version))

    cmd = "rpm -qa|grep cockpit-ovirt"
    cockpit_ovirt_version = run(cmd)
    request.config._environment.append(
        ('cockpit-ovirt', cockpit_ovirt_version))


@pytest.fixture(scope="module")
def firefox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    driver.close()


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
    main_page = MainPage(firefox)
    main_page.check_login_host(host_ip)


def test_18379(firefox):
    """
    RHEVM-18379
        Login into remote machine with "allowUnknown" is default in cockpit
    """
    login_page = LoginPage(firefox)
    login_page.check_allow_unknow_default()


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
    main_page = MainPage(firefox)
    main_page.check_login_host(second_ip)


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
    login_page.check_allow_unknown_true_empty_username()
