from utils.page_objects import PageObject, PageElement

class LoginPage(PageObject):
    """Login page action method come here"""

    brand_log = PageElement(id_="brand")
    

    username = PageElement(id_="login-user-input")
    password = PageElement(id_="login-password-input")
    login_btn = PageElement(id_="login-button")

    def basic_check_elements_exists(self):
        pass
