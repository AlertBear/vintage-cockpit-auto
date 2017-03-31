import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.v41.log_page import LogPage
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


def test_18392(firefox):
    """
    RHEVM-18392
        Check servers status
    """
    log_page = LogPage(firefox)
    log_page.basic_check_elements_exists()
    log_page.check_recent_logs()
    log_page.check_current_boot_logs()
    log_page.check_last_24hours_logs()
    log_page.check_last_7days_logs()
