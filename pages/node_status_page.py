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

    page_links = MultiPageElement(link_text="View")
    accordion_header_btn = MultiPageElement(class_name="accordion-header")
    close_btn = MultiPageElement(class_name="close")

    # elements under Node information dialg
    entry_txts = MultiPageElement(class_name="col-md-6")

    # elements under rollback dialog
    available_layer_txt = MultiPageElement(class_name="col-md-8")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(NodeStatusPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard")
        self.wait(period=5)

    def check_virtual_machine(self):
        """
        Purpose:
            RHEVM-16578
            Check the virtual Machines in oVirt page
        """
        pass

    def check_node_status(self):
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
            time.sleep(10)
            self.health_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list[0:3]:
                i.click()
            time.sleep(3)
            ok_number = len(self.MultiPageElement(class_name="pficon-ok"))
            if ok_number == 13:
                print ("Node health status is ok")
            elif ok_number == 11:
                print ("The node need to register,and node health status is bad")
            else:
                print ("The node health status is error")
            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()

    def check_node_info(self, test_layer):
        """
        Purpose:
            RHEVM-16581
            Check node information in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            self.currentlayer_status_btn.click()
            accordion_header_btn_list = list(self.accordion_header_btn)
            for i in accordion_header_btn_list:
                i.click()
            time.sleep(3)

            # Current layer should be identical with the argument
            entry_txt_list = list(self.entry_txts)
            assert entry_txt_list[1].text == test_layer, \
                "Test layer fail"

            # Since no update action on the new fresh installed
            # system, default layer is current layer
            assert entry_txt_list[0].text == entry_txt_list[1].text, \
                "Default is not current layer"

            close_btn_list = list(self.close_btn)
            for j in close_btn_list[0:]:
                j.click()

    def check_node_layer(self, test_layer):
        """
        Purpose:
            RHEVM-16582
            Check node layers in virtualization dashboard
        """
        pass

    def check_node_rollback(self, test_layer):
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

            assert available_layer_txt_list[0].text == test_layer, \
                "available layer not correct"

            # Check rollback button
            pass

    def check_node_status_fc(self):
        """
        Purpose:
            RHEVM-16584
            Check node status with FC multipath
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.health_status_btn, "Health status btn not exist"
            assert self.currentlayer_status_btn, \
                "Currentlayer status button not exist"
        self.wait()
        pass

    def check_node_status_efi(self):
        """
        Purpose:
            RHEVM-16585
            Check node status with EFI
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.health_status_btn, "Health status btn not exist"
            assert self.currentlayer_status_btn, \
                "Currentlayer status button not exist"
        self.wait()
        pass

    def check_rollabck_func(self):
        """
        Purpose:
            RHEVM-16586
            Rollback funciton in virtualization dashboard
        """
        pass

    def check_network_func(self):
        """
        Purpose:
            RHEVM-16587
            Check the Networking Information in virtualization dashboard
        """
        # Since no network info on cockpit, just drop this case currently
        pass

    def check_system_log(self):
        """
        Purpose:
            RHEVM-16588
            Check the System Logs in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            system_logs_link = page_links_list[1]
            system_logs_link.click()
            time.sleep(3)

    def check_storage(self):
        """
        Purpose:
            RHEVM-16588
            Check the Storage in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            storage_link = page_links_list[2]
            storage_link.click()
            time.sleep(3)

    def check_ssh_key(self):
        """
        Purpose:
            RHEVM-16589
            Check the ssh host key in virtualization dashboard
        """
        self.wait()
        with self.switch_to_frame(self.frame_right_name):
            page_links_list = list(self.page_links)
            storage_link = page_links_list[3]
            storage_link.click()
            time.sleep(3)

    def check_vms(self):
        """
        Purpose:
            RHEVM-16660
            List of vms in dashboard
        """
        # Since it requires to create vms on RHVM, just skip this case
        pass
