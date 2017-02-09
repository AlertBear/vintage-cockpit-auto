import time
from utils.helpers import RhevmAction
from utils.page_objects import PageObject, PageElement, MultiPageElement
from fabric.api import run, get, env


class HePage(PageObject):
    """
    Hosted engine page
    """
    ok_icons = MultiPageElement(class_name="pficon-ok")
    vcenters = MultiPageElement(class_name="vcenter")
    btns = MultiPageElement(tag_name="button")
    panel_titles = MultiPageElement(class_name="panel-title")
    panel_bodys = MultiPageElement(class_name="panel-body")

    vm_state_txt = PageElement(
        xpath=".//*[@class='list-view-pf-additional-info']/div/div")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(SubscriptionsPage, self).__init__(*args, **kwargs)
        self.get("/ovirt-dashboard#/he")
        self.wait(period=10)

    def _query_host_is_registerd(self, rhvm_fqdn, host_name):
        rhvm_action = RhevmAction(rhvm_fqdn)
        result = rhvm_action.query_host_id_by_name(host_name)
        return result

    def add_host_to_rhvm(self, rhvm_fqdn, host_ip, host_name, host_password):
        rhvm_action = RhevmAction(rhvm_fqdn)
        rhvm_action.add_new_host(host_ip, host_name, host_password)
        time.sleep(120)

    def remove_host_from_rhvm(self, rhvm_fqdn, host_name):
        rhvm_action = RhevmAction(rhvm_fqdn)
        rhvm_action.remove_host(host_name)
        time.sleep(10)

    def check_additonal_host(
        self,
        rhvm_fqdn,
        host_ip,
        host_name,
        host_password):
        """
        Purpose:
            Check another host can be added to HE
        """
        r = self._query_host_is_registerd(rhvm_fqdn, host_name)
        assert r, "The host was not added to HE"

    def check_three_buttons(self):
        """
        Purpose:
            Chech three "Maintenance" buttons exist
        """
        assert len(list(self.btns)) == 3, "Maintenance buttons not exist"

    def check_engine_status(self):
        """
        Purpose:
            Check the engine status
        """
        with self.switch_to_frame(self.frame_right_name):
            ok_icons = list(self.ok_icons)
            assert len(ok_icons) == 2, "Hosted engine status not up"

            he_status_txt = list(self.vcenters)[0]
            assert he_status_txt.text == "Hosted Engine is up!", "Hosted engine status not up"

    def check_vm_status(self):
        """
        Purpose:
            Check the host status
        """
        with self.switch_to_frame(self.frame_right_name):
            assert self.vm_state_txt.text == "State: up" "The VM is not up"

    def check_he_running_on_host(self, host_ip):
        cmd = "hostname"
        hostname = run(cmd)
        with self.switch_to_frame(self.frame_right_name):
            he_running_on_txt = list(self.vcenters)[1]
            assert he_running_on_txt.text == "Hosted Engine is running on %s" \
                % hostname, "Hosted engine running on host not correct"
