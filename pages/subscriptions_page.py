import time
# from selenium import webdriver
# from pages.login_page import LoginPage
from utils.page_objects import PageObject,PageElement,MultiPageElement

class SubscriptionsPage(PageObject):
    """Subscription-manager for host to register to RHSM/Satelliate server"""

    # Elements on subscriptions page
    # 
    #
    #
    need_registered_msg = PageElement(xpath="//div[@id='subscriptions-unregistered']/span")
    register_btn = PageElement(id_="subscriptions-register")


    def __init__(self, *args, **kwargs):
        super(SubscriptionsPage, self).__init__(*args, **kwargs)
        self.get("/subscriptions")


    def basic_check_elements_exists(self):
        assert self.need_registered_msg, "system must be registered message not exist"
        assert self.register_btn, "register system btn not exist"

    def register_to_rhsm(self):
        self.register_system_btn.click()
        time.sleep(1)