import time
import re
from utils.page_objects import PageObject, PageElement


class MainPage(PageObject):
    """Login page action method come here"""

    brand_log = PageElement(id_="index-brand")
    machine_link = PageElement(
        xpath=".//*[@id='machine-link']/span")

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)
        self.get("/system")
        self.wait_until_element_visible(self.brand_log)

    def basic_check_elements_exists(self):
        assert self.brand_log, "brand-log not exist"
        time.sleep(2)

    def check_login_host(self, host_ip):
        assert re.search(host_ip, self.machine_link),   \
            "%s not login" % host_ip
