import time
import re
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import run, settings

class SystemPage(PageObject):
    targets_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[1]")
    sys_service_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[2]")
    sockets_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[3]")
    timers_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[4]")
    paths_btn = PageElement(
        xpath=".//*[@id='services-filter']/button[5]")

    # Elements under the system service button
    fcoe_service = PageElement(
        xpath=".//*[@tag_name='tbody']/tr[1]/td/span")

    # Elements after click above service button
    service_title_name = PageElement(
        xpath=".//*[@id='service']/ol/li/")
    service_start_stop_action = PageElement(
        xpath=".//*[@id='service-unit-action']/button[1]")
    service_enable_disable_action = PageElement(
        xpath=".//*[@id='service-file-action']/button[1]")
    service_unit_dropdown_action = PageElement(
        xpath=".//*[@id='service-unit-action']/button[2]")
    service_file_dropdown_action = PageElement(
        xpath=".//*[@id='service-file-action']/button[2]")

    service_units = MultiPageElement(xpath=".//*[@tag_name='li']/a")

    # frame name
    frame_right_name = "cockpit1:localhost/system"

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)
        self.get("/system/services")
        self.wait_until_element_visible(self.brand_log)

    def basic_check_elements_exists(self):
        assert self.targets_btn, "targets button not exists"
        assert self.sys_service_btn, "system service button not exists"
        assert self.sockets_btn, "socket button not exists"
        assert self.timers_btn, "timers button not exists"
        assert self.paths_btn, "paths button not exists"

    def check_service_disable(self):
        with self.switch_to_frame(self.frame_right_name):
            self.fcoe_service.click()
            time.sleep(1)
            self.service_enable_disable_action.click()

        with settings(warn_only=True):
            cmd = "service fcoe.service status|grep Loaded"
            output2 = run(cmd)

        assert re.search("disabled", output2.split(';')[1]),   \
            "Failed to disable the fcoe service"

    def check_service_enable(self):
        with self.switch_to_frame(self.frame_right_name):
            self.fcoe_service.click()
            time.sleep(1)
            self.service_enable_disable_action.click()

        with settings(warn_only=True):
            cmd = "service fcoe.service status|grep Loaded"
            output2 = run(cmd)

        assert re.search("enabled", output2.split(';')[1]),   \
            "Failed to enable the fcoe service"

    def check_service_stop(self):
        with self.switch_to_frame(self.frame_right_name):
            self.fcoe_service.click()
            time.sleep(1)
            self.service_start_stop_action.click()

        with settings(warn_only=True):
            cmd = "service fcoe.service status|grep Active"
            output1 = run(cmd)

        assert re.search("inactive", output1),   \
            "Failed to stop the fcoe service"

    def check_service_start(self):
        with self.switch_to_frame(self.frame_right_name):
            self.fcoe_service.click()
            time.sleep(1)
            self.service_start_stop_action.click()

        with settings(warn_only=True):
            cmd = "service fcoe.service status|grep Active"
            output1 = run(cmd)

        assert re.search("active", output1),   \
            "Failed to start the fcoe service"

    def check_service_restart(self):
        with self.switch_to_frame(self.frame_right_name):
            self.fcoe_service.click()
            time.sleep(1)
            self.service_unit_dropdown_action.click()

            # Restart unit action
            list(self.service_units)[2].click()
        with settings(warn_only=True):
            cmd = "service fcoe.service status|grep Active"
            output1 = run(cmd)

        assert re.search("active", output1),   \
            "Failed to restart the fcoe service"
