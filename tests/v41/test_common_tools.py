import pytest
import time
from selenium import webdriver
from pages.login_page import LoginPage
from pages.v41.tools_account_page import AccountPage
from pages.v41.tools_diagnostic_page import DiagnosticPage
from fabric.api import run, env, settings
from conf import *


host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD

ROOT_URI = "https://" + host_ip + ":9090"

env.host_string = host_user + '@' + host_ip
env.password = host_password


@pytest.fixture(autouse=True)
def _environment(request):
    with settings(warn_only=True):
        cmd = "rpm -q cockpit-ovirt-dashboard"
        cockpit_ovirt_version = run(cmd)
        print cockpit_ovirt_version
        request.config._environment.append((
            'cockpit-ovirt', cockpit_ovirt_version))

        cmd = "rpm -q imgbased"
        result = run(cmd)
        if result.failed:
            cmd = "cat /etc/redhat-release"
            redhat_release = run(cmd)
            request.config._environment.append((
                'redhat-release', redhat_release))
        else:
            cmd = "imgbase w"
            output_imgbase = run(cmd)
            rhvh_version = output_imgbase.split()[-1].split('+')[0]
            request.config._environment.append((
                'rhvh-version', rhvh_version))


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


def test_18410(firefox):
    """
    RHEVM-18410
        Create account in cockpit
    """
    accout_page = AccountPage(firefox)
    accout_page.create_new_account()
    accout_page.check_new_account_from_ssh(host_ip)
    accout_page.delete_new_account()


def test_18416(firefox):
    """
    RHEVM-18416
        Create diagnositc in cockpit
    """
    diagnostic_page = DiagnosticPage(firefox)
    diagnostic_page.create_sos_report()
    time.sleep(30)
    diagnostic_page.check_sosreport_can_be_downloaded()
