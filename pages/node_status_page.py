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
    rollback_btn = PageElement(
        xpath=".//*[@id='content']/div/div/div[1]/table/tbody[2]/tr[2]/td[2]/div[1]/span/button")
    accordion_header_btn = MultiPageElement(class_name="accordion-header")
    close_btn = MultiPageElement(class_name="close")

    # elements under Node information dialg
    entry_txts = MultiPageElement(class_name="col-md-6 entry")

    # elements under rollback dialog
    available_layer_txt = MultiPageElement(class_name="col-md-8")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(NodeStatusPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard")
        self.wait(period=5)

    def basic_check_elements_exists(self):
        """
        Purpose:
            RHEVM-16579
            Check node status in virtualization dashboard.
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.health_status_btn, "Health status btn not exist"
            assert self.currentlayer_status_btn, \
                "Currentlayer status button not exist"
        self.wait()

    def check_node_health(self):
        """
        Purpose:
            RHEVM-16580
            Check node health info in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.health_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list[0:3]:
                i.click()
            time.sleep(3)
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

    def check_node_info(self):
        """
        Purpose:
            RHEVM-16581
            Check node information in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.currentlayer_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list[0:]:
                i.click()
            time.sleep(3)
            entry_txt_list = list(self.entry_txts)
            for txt in entry_txt_list[0:]:
                print txt.text
                assert txt.text is None, "failure"
                # pass, still has bug
            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()

    def check_node_rollback(self):
        """
        Purpose:
            RHEVM-16583
            Check node rollback in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.rollback_btn.click()
            time.sleep(3)
            available_layer_txt_list = list(self.available_layer_txt)
            for ava in available_layer_txt_list[0:]:
                print ava.text
