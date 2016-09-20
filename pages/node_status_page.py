""""""
import time
from utils.page_objects import PageObject, PageElement, MultiPageElement


class NodeStatusPage(PageObject):
    """ To check Node status and System info on Virtualization panel."""

    # health_status_btn: click health_status_text link_text
    # currentlayer_status_btn: click currentlayer_status_text link_text
    # accordion_header_btn: like "Thin storage","basic storage","Mount points" button
    # close_btn : close button,like "X"

    health_status_btn = PageElement(
        xpath=".//*[@id='content']/div/div/div[1]/table/tbody[2]/tr[1]/td[2]/div[1]/a/div")
    currentlayer_status_btn = PageElement(
        xpath=".//*[@id='content']/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]/a")
    accordion_header_btn = MultiPageElement(class_name="accordion-header")
    close_btn = MultiPageElement(class_name="close")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(NodeStatusPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard")
        self.wait(period=5)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            assert self.health_status_btn, "Health status btn not exist"
            assert self.currentlayer_status_btn, "Currentlayer status button not exist"
        self.wait()

    # function_1: check node health
    def check_node_health(self):
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.health_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list[0:3]:
                i.click()
            time.sleep(2)
            ok_number = len(MultiPageElement(class_name="pficon-ok"))
            if ok_number == 13:
                print ("Node health status is ok")
            elif ok_number == 11:
                print ("The node need to register,and node health status is bad")
            else:
                print ("The node health status is error")
            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()
