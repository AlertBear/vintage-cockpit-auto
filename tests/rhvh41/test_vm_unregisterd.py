import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.rhvh41.virtual_machines_page import VirtualMachinesPage
from conf import *

host_ip = HOST_IP
host_user = HOST_USER
host_password = HOST_PASSWORD

ROOT_URI = "https://" + host_ip + ":9090"


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
    login_page.login_with_credential(host_user, host_password)

def test_running_virtual_machines_unregister(firfox):
    virtual_machines_page = VirtualMachinesPage(firfox)
    virtual_machines_page.basic_check_elements_exists()
    virtual_machines_page.check_running_vms_unregister()

def test_virtual_machines_in_cluster_unregister(firfox):
    virtual_machines_page = VirtualMachinesPage(firfox)
    virtual_machines_page.basic_check_elements_exists()
    virtual_machines_page.check_vms_in_cluster_unregister()

def test_virtual_machines_vdsm(firfox):
    virtual_machines_page = VirtualMachinesPage(firfox)
    virtual_machines_page.basic_check_elements_exists()
    virtual_machines_page.check_vdsm_elements()
    virtual_machines_page.check_vdsm_conf_edit()
