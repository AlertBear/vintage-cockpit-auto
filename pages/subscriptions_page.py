import time
import os,re
from utils.page_objects import PageObject, PageElement
from terminal_page import TerminalPage
from fabric.api import settings, run, env, get
from StringIO import StringIO

env.host_string = 'root@10.66.8.149'
env.password = 'redhat'
ca_path = "https://10.73.75.134/pub/katello-ca-consumer-satellite61.redhat.com-1.0-1.noarch.rpm"

class SubscriptionsPage(PageObject):
    """Subscription-manager for host to register to RHSM/Satellite server"""

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
        """
        Purpose:
            RHEVM-16598
            Test subscription to RHSM
        """
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self.__clean_all()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.url_input.send_keys("subscription.rhn.redhat.com")
            self.login_input.send_keys("qa@redhat.com")
            self.passwd_input.send_keys("NWmfx9m28UWzxuvh")
            self.register_btn.click()
            time.sleep(50)

    # function_2: register to rhsm with activation key and organization
    def register_rhsm_key_org(self):
        """
        Purpose:
            RHEVM-17034
            Test subscription to RHSM with key and organization
        """
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self.__clean_all()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.url_input.send_keys("subscription.rhn.redhat.com")
            self.key_input.send_keys("rhevh")
            self.org_input.send_keys("711497")
            self.register_btn.click()
            time.sleep(40)

    # function_3: register to satellite with custom url.
    def register_satellite(self):
        """
        Purpose:
            RHEVM-16752
            Test subscription to Satellite server
        """
        with self.switch_to_frame(self.frame_right_name):
            self.register_sys_btn.click()
            self.__clean_all()
            self.url_select_btn.click()
            self.url_custom_item.click()
            self.url_input.send_keys("satellite61.redhat.com/rhsm")
            # add funciton to install CA to host
            self.login_input.send_keys("admin")
            self.passwd_input.send_keys("redhat")
            self.register_btn.click()
            time.sleep(40)
    
    def check_password_encrypted(self):
        """
        Purpose:
            RHEVM-16750
            Test check password is encrypted in rhsm.log
        """
        remote_path = "/var/log/rhsm/rhsm.log"
        fd = StringIO()
        get(remote_path, fd)
        content=fd.getvalue()
        assert not re.search("NWmfx9m28UWzxuvh", content), "There is plain password in rhsm.log file"

    # function_4: Check subscription result
    def check_subscription_result(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.product_name.text == "Red Hat Virtualization Host", \
                "product name is wrong"
            assert self.register_status.text == "Subscribed", \
                "subscription fail"

    # function_5: subscription-manager unregister
    def unregister_subsciption(self):
        cmd = 'subscription-manager unregister'
        subscripted = run(cmd)
        time.sleep(5)
        if subscripted != "System has been unregistered":
            time.sleep(5)
    
    # function_6: Install ca for host
    def ca_install(self):
        cmd_download_ca = "curl -O -k " + ca_path
        downloaded = run(cmd_download_ca)
        time.sleep(5)
        cmd_install_ca = "rpm -Uvh " + os.path.basename(ca_path)
        run(cmd_install_ca)
        time.sleep(7)
    
    # function_6: Clean all textarea's input.
    def __clean_all(self):
        self.login_input.clear()
        self.passwd_input.clear()
        self.key_input.clear()
        self.org_input.clear()

    # function_7: Reset environment for register RHSM.
    def reset(self):
        cmd_rpm_qa = "rpm -qa|grep katello"
        result = run(cmd_rpm_qa)
        if result:
            cmd = "rpm -e " + os.path.splitext(os.path.basename(ca_path))[0]
            run(cmd)
            time.sleep(2)
