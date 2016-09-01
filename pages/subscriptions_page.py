import time
import os
from utils.page_objects import PageObject, PageElement


class SubscriptionsPage(PageObject):
    """Subscription-manager for host to register to RHSM/Satellite server"""

    ######################
    # Elements on subscriptions page
    #
    # need_registered_msg: ...
    # register_btn: "Register system" button
    # login_input: username text editor
    # passwd_input: password text editor
    # key_input: activation key text editor
    # org_input: organization text editor
    # register_btn: "Register" button
    # cancel_btn: "Cancel" button
    # url_select_btn: URL select list button
    # url_default_item: URL select list item "Default"
    # url_custom_item: URL select list item "Custom URL"
    # url_input: URL text editor
    #
    ######################

    need_registered_msg = PageElement(
        xpath="//div[@id='subscriptions-unregistered']/span")
    register_sys_btn = PageElement(id_="subscriptions-register")
    login_input = PageElement(id_="subscription-register-username")
    passwd_input = PageElement(id_="subscription-register-password")
    key_input = PageElement(id_="subscription-register-key")
    org_input = PageElement(id_="subscription-register-org")
    register_btn = PageElement(id_="account-register-start")
    cancel_btn = PageElement(class_name="btn btn-default")
    # url = PageElement(id_="subscription-register-url")
    url_select_btn = PageElement(
        xpath=".//*[@id='subscription-register-url']/button")
    url_default_item = PageElement(
        xpath=".//*[@id='subscription-register-url']/ul/li[1]/a")
    url_custom_item = PageElement(
        xpath=".//*[@id='subscription-register-url']/ul/li[2]/a")
    url_input = PageElement(id_="subscription-register-url-custom")
    product_name = PageElement(
        xpath=".//*[@id='subscriptions-subscribed']/div/div[2]/table/tbody/tr[1]/td[2]/span")
    register_status = PageElement(
        xpath=".//*[@id='subscriptions-subscribed']/div/div[2]/table/tbody/tr[5]/td[2]/span")
    # frame name
    frame_right_name = "cockpit1:localhost/subscriptions"

    def __init__(self, *args, **kwargs):
        super(SubscriptionsPage, self).__init__(*args, **kwargs)
        self.get("/subscriptions")

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.need_registered_msg, \
                "system must be registered message not exist"
            assert self.register_sys_btn, "register system btn not exist"
            assert self.login_input, "login text editor not exist"
            assert self.passwd_input, "password text editor not exist"
            assert self.register_btn, "register button not exist"
            assert self.key_input, "Activation Key text editor not exist"
            assert self.org_input, "Organization text editor not exist"
            assert self.url_select_btn, "Url select btn not exist"
            assert self.url_default_item, "default item in url list not exist"
            assert self.url_custom_item, "custom item in url list not exist"
            assert self.url_input, "url text editor not exist"

    # function_1: register to rhsm with username and password
    def register_rhsm(self):
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self.login_input.send_keys("qa@redhat.com")
            self.passwd_input.send_keys("NWmfx9m28UWzxuvh")
            self.register_btn.click()
            time.sleep(30)

    # function_2: register to rhsm with activation key and organization
    def register_rhsm_key_org(self):
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self.key_input.send_keys("rhevh")
            self.org_input.send_keys("Quality Assurance")
            self.register_btn.click()
            time.sleep(20)

    # function_3: register to satellite with custom url.
    # need to modify
    def register_satellite(self):
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.url_input.send_keys("satellite61.redhat.com/rhsm")
            # add funciton to install CA to host
            self.login_input.send_keys("admin")
            self.passwd_input.send_keys("redhat")
            self.register_btn.click()

    # function_4: Check subscription result
    def check_subscription_result(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.product_name.text == "Red Hat Virtualization Host", \
                "product name is wrong"
            assert self.register_status.text == "Subscribed", \
                "subscription fail"

    # function_5: subscription-manager unregister
    def unregister_subsciption(self):
        # wait for Terminal page finished
        pass
