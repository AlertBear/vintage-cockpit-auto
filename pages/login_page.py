""""""
from utils.page_objects import PageObject, PageElement


class LoginPage(PageObject):
    """Login page action method come here"""

    brand_log = PageElement(id_="brand")

    username_input = PageElement(id_="login-user-input")
    password_input = PageElement(id_="login-password-input")
    login_btn = PageElement(id_="login-button")

    def __init__(self, *args, **kwargs):
        super(LoginPage, self).__init__(*args, **kwargs)
        self.get("/")
        self.wait_until_element_visible(self.username_input)

    def basic_check_elements_exists(self):
        assert self.username_input, "input username not exist"
        assert self.password_input, "input password not exist"
        assert self.login_btn, "login btn not exist"
        self.wait()

    def login_with_credential(self, username, password):
        self.username_input.send_keys(username)
        self.password_input.send_keys(password)
        self.login_btn.click()
        self.wait()
