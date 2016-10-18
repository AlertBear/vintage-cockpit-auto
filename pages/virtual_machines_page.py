import re
import time
from utils.page_objects import PageObject, PageElement
from utils.helpers import RhevmAction
from selenium.common.exceptions import NoAlertPresentException
from fabric.api import run, env, get
from StringIO import StringIO

env.host_string = 'root@10.66.8.149'
env.password = 'redhat'
str_input = "#some_text"
rhevm_fqdn = "rhevm-40-1.englab.nay.redhat.com"
rhvh_credentials = ["10.66.8.149", "dhcp-8-149.nay.redhat.com", "redhat"]
rhvh_nfs = ['10.66.65.30','/home/wangwei/nfs','dhcp-8-149.nay.redhat.com']

class VirtualMachinesPage(PageObject):
    """
    Function:
        Inspect virtual machines which managed by RHEVM in cockpit WebUI
    """

    running_vms_btn = PageElement(id_="main-btn-menu-hostvms")
    vms_in_cluster_btn = PageElement(id_="main-btn-menu-allvms")
    vdsm_btn = PageElement(id_="main-btn-menu-vdsm")

    technical_preview_text = PageElement(xpath=".//*[@id='ovirt-content']/table/tbody/tr/td[2]/div")
    engine_login_link = PageElement(link_text="Login to Engine")
    maintenance_host_link = PageElement(link_text="Host to Maintenance")
    refresh_link = PageElement(partial_link_text="Refresh")

    virtual_machines_title = PageElement(xpath=".//*[@id='virtual-machines']/div[1]/div/div[1]/h3")
    total_vms_text = PageElement(id_="host-vms-total")
    vdsm_unactived_textblock = PageElement(id_="vdsm-is-not-active")

    vdsm_service_management_link = PageElement(link_text="VDSM Service Management")
    vdsm_conf_textarea = PageElement(id_="editor-vdsm-conf")
    vdsm_save_btn = PageElement(id_="editor-vdsm-btn-save")
    vdsm_reload_btn = PageElement(id_="editor-vdsm-btn-reload")

    vdsm_config_dialog_title = PageElement(id_="modal-confirmation-title")
    vdsm_config_dialog_close_btn = PageElement(class_name="close")
    vdsm_config_dialog_text = PageElement(id_="modal-confirmation-text")
    vdsm_config_dialog_ok = PageElement(id_="modal-confirmation-ok")
    vdsm_config_dialog_cancel = PageElement(xpath=".//*[@id='modal-confirmation']/div/div/div[3]/button[1]")
    vdsm_config_dialog_saved = PageElement(id_="editor-vds-conf-msg")
    
    #sub-frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(VirtualMachinesPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard#/management")
        self.wait(period=10)

        self.rhevm_action_obj = RhevmAction(rhevm_fqdn)

    def basic_check_elements_exists(self):
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            assert self.running_vms_btn, "Running VMs button is missing"
            assert self.vms_in_cluster_btn, "VMs in cluster button is missing"
            assert self.vdsm_btn, "VDSM button is missing"
            assert self.engine_login_link, "Login to engine link is missing"
            assert self.maintenance_host_link, "Host to maintenance link is missing"
            assert self.refresh_link, "Refresh link is missing"

    # function_1: Check vms when host unregister to RHEVM
    def check_running_vms_unregister(self):
        """
        Purpose:
            RHEVM-17065
            Check running VMs (Unregister to RHEVM) status in virtual machines page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            assert re.search("Virtual Machines", self.virtual_machines_title.text),\
             "Running VMs page title is wrong"
            assert self.total_vms_text.text == "0", "Total VMs number is displayed wrong"
            target_textblock = "The VDSM service is not responding on this host"
            assert re.search(target_textblock, self.vdsm_unactived_textblock.text), \
            "The VDSM service is responding on this host"

    # function_2: Check vms in cluster when host unregister to RHEVM
    def check_vms_in_cluster_unregister(self):
        """
        Purpose:
            RHEVM-17066
            Check VMs in cluster (Unregister to RHEVM) status in virtual machines page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vms_in_cluster_btn.click()
            self.wait(period=1)
            try:
                assert self.w.switch_to_alert()
            except NoAlertPresentException as e: 
                raise e
    
    # function_3: Check vms when host register to RHEVM
    # def check_running_vms_register(self):
    #     """
    #     Purpose:
    #         RHEVM-16607
    #         Check running VMs(local storage disk image) status in virtual machines page
    #     """
    #     with self.switch_to_frame(self.frame_right_name):
    #         self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
    #         # if self.rhevm_action_obj:
    #         #     if self.rhevm_action_obj.add_new_host(*rhvh_credentials):
    #         #         print 'Host regitst to RHEVM successfully'
    #         #         if self.rhevm_action_obj.add_nfs_data_storage(*rhvh_nfs):
    #         #             self.rhevm_action_obj.create_vm("vm_1")
    #         #         else:
    #         #             print "Add nfs data storage failed"
    #         #     else:
    #         #         print "Add new host failed"
    #         # else:
    #         #     print "Create rhevm_action object failed"
    #         self.rhevm_action_obj.create_vm("vm1")


    # function_3: Check vdsm page elements are exist
    def check_vdsm_elements(self):
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            assert self.vdsm_service_management_link, "The VDSM service management link is missing"
            assert self.vdsm_conf_textarea, "The VDSM config editor is missing"
            assert self.vdsm_save_btn, "The VDSM config editor save button is missing"
            assert self.vdsm_reload_btn, "The VDSM config editor reload button is missing"

    # function_4: Check vdsm textarea is editable
    def check_vdsm_conf_edit(self):
        """
        Purpose:
            RHEVM-16610
            Check VDSM info in virtual machines page
        """
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            self._edit_vdsm_conf(str_input)
            assert self.vdsm_conf_textarea.get_attribute('value').endswith("some_text"), \
            "Edit vdsm.conf textarea failed"
            self.wait(period=1)
            self._vdsm_conf_confirm(self.vdsm_reload_btn)
            self._vdsm_conf_confirm(self.vdsm_save_btn)
            if not self._check_vdsm_conf_host():
                print "edit operation is successful"
            #TODO: Add VDSM service Management link testing

    # function_5: Check save function of vdsm page
    def check_vdsm_conf_save(self):
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            if self.vdsm_save_btn:
                self._check_vdsm_config_dialog(self.vdsm_save_btn)
    
    # function_6: Check reload function of vdsm page
    def check_vdsm_conf_reload(self):
        with self.switch_to_frame(self.frame_right_name):
            self.w.switch_to_frame(self.w.find_element_by_tag_name("iframe"))
            self.vdsm_btn.click()
            if self.vdsm_reload_btn:
                self._check_vdsm_config_dialog(self.vdsm_reload_btn)

    # function_7: Append text to vdsm.conf
    def _edit_vdsm_conf(self, input):
        self.vdsm_conf_textarea.send_keys(input)

    # function_8: Check dialogue in vdsm page
    def _check_vdsm_config_dialog(self, button):
        button.click()
        self.wait(period=1)
        if button.text == 'Save':
            assert re.search("Save to vdsm.conf", self.vdsm_config_dialog_title.\
                get_attribute('innerHTML')), "Dialogue is not save to vdsm.conf"
            assert self.vdsm_config_dialog_text.get_attribute('innerHTML').startswith(\
                "Content of vdsm.conf file will be replaced."), "Dialogue text is wrong!"
        elif button.text == "Reload":
            assert re.search("Reload stored vdsm.conf", self.vdsm_config_dialog_title.\
                get_attribute('innerHTML')), "Dialogue is not reload stored vdsm.conf"
            assert self.vdsm_config_dialog_text.get_attribute('innerHTML').startswith(\
                "Content of vdsm.conf will be reloaded, unsaved changes will be lost."), "Dialogue text is wrong!"
        assert self.vdsm_config_dialog_ok, "Save button is missing in the dialogue"
        assert self.vdsm_config_dialog_cancel, "Cancel button is missing in the dialogue"
            
        if self.vdsm_config_dialog_cancel.click():
            self.wait(period=1)
            print "The function of cancel button in vdsm.conf dialogue is invalid"
            self.wait(period=1)
        else:
            self.wait(period=1)
        button.click()
        self.wait(period=1)
        if self.vdsm_config_dialog_ok.click():
            self.wait(period=1)
            print "The function of cancel button in vdsm.conf dialogue is invalid"
            self.wait(period=1)
        else:
            self.wait(period=1)
            if button.text == 'Save':
                assert re.search("Saved", self.vdsm_config_dialog_saved.text), \
                "Save to vdsm.conf failed"
            elif button.text == 'Reload':
                assert re.search("Loaded", self.vdsm_config_dialog_saved.text), \
                "Load to vdsm.conf failed"
            self.wait(period=5)
            assert re.search("", self.vdsm_config_dialog_saved.text)
    
    # function_8: confirm dialogue
    def _vdsm_conf_confirm(self, button):
        button.click()
        self.wait(period=1)
        self.vdsm_config_dialog_ok.click()
        self.wait(period=2)
    
    # function_9: check vdsm configurate file on remote host
    def _check_vdsm_conf_host(self):
        remote_path = "/etc/vdsm/vdsm.conf"
        fd = StringIO()
        get(remote_path, fd)
        content = fd.getvalue()
        assert not re.search(str_input, content), "Edit & Save vdsm.conf failed"
