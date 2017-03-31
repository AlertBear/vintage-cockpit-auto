import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.v41.dashboard_page import DashboardPage
from fabric.api import run, env
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


def test_login(firefox):
    login_page = LoginPage(firefox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential(host_user, host_password)


def test_18372(firefox):
    """
    RHEVM-18372
        CPU shown in cockpit page
    """
    dashboard_page = DashboardPage(firefox)
    dashboard_page.check_cpu()


def test_18373(firefox):
    """
    RHEVM-18373
        Memory shown in cockpit page
    """
    dashboard_page = DashboardPage(firefox)
    dashboard_page.check_memory()


def test_18374(firefox):
    """
    RHEVM-18372
        Network shown in cockpit page
    """
    dashboard_page = DashboardPage(firefox)
    dashboard_page.check_network()


def test_18375(firefox):
    """
    RHEVM-18372
        Disk IO shown in cockpit page
    """
    dashboard_page = DashboardPage(firefox)
    dashboard_page.check_disk_io()


def test_18371(firefox):
    """
    RHEVM-18372
        Servers can be added in Dashboard page
    """
    # To do:
    dashboard_page = DashboardPage(firefox)
    dashboard_page.check_server_can_be_added(second_ip, second_password)
