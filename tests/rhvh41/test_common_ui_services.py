import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh41.service_page import ServicePage
from fabric.api import run, env
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


def test_login(firefox):
    login_page = LoginPage(firefox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def test_18392(firefox):
    """
    RHEVM-18392
        Check servers status
    """
    service_page = ServicePage(firefox)
    service_page.check_service_disable()
    time.sleep(1)
    service_page.check_service_enable()
    time.sleep(1)
    service_page.check_service_stop()
    time.sleep(1)
    service_page.check_service_start()
    time.sleep(1)
    service_page.check_service_restart()
    time.sleep(1)
