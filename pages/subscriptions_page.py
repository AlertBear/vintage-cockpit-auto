from utils.page_objects import PageObject, PageElement


class SubscriptionsPage(PageObject):
    """Subscription-manager for host to register to RHSM/Satelliate server"""

    # Elements on subscriptions page

    need_registered_msg = PageElement(xpath="//div[@id='subscriptions-unregistered']/span")
    register_btn = PageElement(id_="subscriptions-register")

    frame_right_name = "cockpit1:localhost/subscriptions"

    def __init__(self, *args, **kwargs):
        super(SubscriptionsPage, self).__init__(*args, **kwargs)
        self.get("/subscriptions")
        self.wait(period=10)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.need_registered_msg, "system must be registered message not exist"
            assert self.register_btn, "register system btn not exist"

    def register_to_rhsm(self):
        with self.switch_to_frame(self.frame_right_name):
            self.register_btn.click()
        self.wait()
