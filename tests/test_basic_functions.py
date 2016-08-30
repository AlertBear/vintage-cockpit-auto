import time
import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.main_page import MainPage


ROOT_URI = "https://192.168.15.112:9090"

@pytest.fixture(scope="module")
def firfox(request):
    driver = webdriver.Firefox()
    driver.implicitly_wait(20)
    root_uri = getattr(request.module, "ROOT_URI", None)
    driver.root_uri = root_uri
    yield driver
    # driver.close()


def test_login_page(firfox):
    login_page = LoginPage(firfox)
    login_page.basic_check_elements_exists()
    login_page.login_with_credential()
    time.sleep(3)

def test_main_page(firfox):
    main_page = MainPage(firfox)
    main_page.basic_check_elements_exists()