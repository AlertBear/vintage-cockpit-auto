import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.virtual_machines_page import VirtualMachinesPage


ROOT_URI = "https://10.66.8.149:9090"


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

# def test_running_virtual_machines_unregister(firfox):
#     virtual_machines_page = VirtualMachinesPage(firfox)
#     virtual_machines_page.basic_check_elements_exists()
#     virtual_machines_page.check_running_vms_unregister()

# def test_virtual_machines_in_cluster_unregister(firfox):
#     virtual_machines_page = VirtualMachinesPage(firfox)
#     virtual_machines_page.basic_check_elements_exists()
#     virtual_machines_page.check_vms_in_cluster_unregister()

# def test_virtual_machines_vdsm(firfox):
#     virtual_machines_page = VirtualMachinesPage(firfox)
#     virtual_machines_page.basic_check_elements_exists()
#     virtual_machines_page.check_vdsm_elements()
#     virtual_machines_page.check_vdsm_conf_edit()

def test_running_virtual_machines_register(firfox):
    virtual_machines_page = VirtualMachinesPage(firfox)
    virtual_machines_page.check_running_vms_register()
