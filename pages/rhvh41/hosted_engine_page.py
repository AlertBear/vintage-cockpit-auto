import time
from utils.helpers import RhevmAction
from utils.page_objects import PageObject, MultiPageElement
from fabric.api import run, env, settings


class HePage(PageObject):
    """
    Hosted engine page
    """
    ok_icons = MultiPageElement(class_name="pficon-ok")
    vcenters = MultiPageElement(class_name="vcenter")
    btns = MultiPageElement(class_name="btn-default")
    panel_titles = MultiPageElement(class_name="panel-title")
    panel_bodys = MultiPageElement(class_name="panel-body")

    vm_state_txts = MultiPageElement(
        xpath=".//*[@class='list-view-pf-additional-info']/div/div")
    list_group_item_txts = MultiPageElement(class_name= "list-group-item-text")

    # frame name
    frame_right_name = "cockpit1:localhost/ovirt-dashboard"

    def __init__(self, *args, **kwargs):
        super(HePage, self).__init__(*args, **kwargs)
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
        print len(list(self.btns))
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
            assert he_status_txt.text.strip() == "Hosted Engine is up!", "Hosted engine status not up"

    def check_vm_status(self):
        """
        Purpose:
            Check the host status
        """
        with self.switch_to_frame(self.frame_right_name):
            print list(self.vm_state_txts)[0].text.split()[-1]
            assert list(self.vm_state_txts)[0].text.split()[-1] == "up" "The VM is not up"

    def check_he_running_on_host(self, host_ip):
        """
        Purpose:
            Check the hosted engine is running on local host
        """
        cmd = "hostname"
        hostname = run(cmd)
        with self.switch_to_frame(self.frame_right_name):
            he_running_on_txt = list(self.vcenters)[1]
            assert he_running_on_txt.text == "Hosted Engine is running on %s" \
                % hostname, "Hosted engine running on host not correct"

    def check_put_host_to_local_maintenance(self):
        """
        Purpose:
            Put the host to local maintenance
        """
        with self.switch_to_frame(self.frame_right_name):
            put_host_local_maintenace_btn = list(self.btns)[0]
            put_host_local_maintenace_btn.click()
            time.sleep(60)

            host_agent_maintenance_txt = list(self.list_group_item_txts)[0].text
            host_maintenance_txt = host_agent_maintenance_txt.split()[-1]
            if host_maintenance_txt == "false":
                with settings(warn_only=True):
                    cmd = "hosted-engine --set-maintenance --mode=local"
                    result = run(cmd)
                    print result.stderr
                assert result.succeeded, "Failed to put host to local maintenance"

    def check_vm_migraged(self):
        """
            Suppose there are only two hosts,
            check the HE vm already migrate to another host
        """
        with self.switch_to_frame(self.frame_right_name):
            host_agent_maintenance_txt = list(self.list_group_item_txts)[1].text
            host_maintenance_txt = host_agent_maintenance_txt.split()[-1]
            assert host_maintenance_txt == "true",  \
                "The HE vm did not migrated to another host"
