""""""
import time
from utils.page_objects import PageObject, PageElement


class LoginPage(PageObject):
    """Login page action method come here"""

    brand_log = PageElement(id_="brand")

    username = PageElement(id_="login-user-input")
    password = PageElement(id_="login-password-input")
    login_btn = PageElement(id_="login-button")

    def __init__(self, *args, **kwargs):
        super(LoginPage, self).__init__(*args, **kwargs)
        self.get("/")
        time.sleep(2)

    def basic_check_elements_exists(self):
        assert self.username, "input username not exist"
        assert self.password, "input password not exist"
        assert self.login_btn, "login btn not exist"
        time.sleep(2)

    def login_with_credential(self):
        self.username.send_keys("root")
        self.password.send_keys("redhat")
        self.login_btn.click()
        time.sleep(2)
