#
# RHVH4.1 test scenarios contains only one case
#
rhvh41_common_ui = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [
        "dell-pet105-02.qe.lab.eng.nay.redhat.com",
        "hp-z620-04.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": [
        "tests/rhvh41/test_common_ui_dashboard.py",
        "tests/rhvh41/test_common_ui_system.py"]
}

rhvh41_common_tools = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [
        "dell-pet105-02.qe.lab.eng.nay.redhat.com",
        "hp-z620-04.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_common_tools_subscription.py"]
}

rhvh41_dashboard = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [
        "dell-pet105-02.qe.lab.eng.nay.redhat.com",
        "hp-z620-04.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": [
        "tests/rhvh41/test_dashboard_nodectl.py",
        "tests/rhvh41/test_dashboard_ui.py"]
}

rhvh41_dashboard_ui_uefi = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_dashboard_ui_efi.py"]
}

rhvh41_dashboard_ui_fc = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_dashboard_ui_fc.py"],
}

rhvh41_he_install = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_he_install.py"]
}

rhvh41_he_install_bond = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_he_install_bond.py"]
}

rhvh41_he_install_bv = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_he_install_bv.py"]
}

rhvh41_he_install_vlan = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": [],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_he_install_vlan.py"]
}

rhvh41_he_install_non_default_port = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_he_install_non_default_port.py"]
}

rhvh41_vm_unregister = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_vm_unregister.py"]
}

#
# RHVH4.1 test scenario contains multiple cases
#
rhvh41_tier1 = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_CASES": [],
    "CASES": [
        "tests/rhvh41/test_dashboard_nodectl.py",
        "tests/rhvh41/test_dashboard_ui.py",
        "tests/rhvh41/test_vm_unregisterd.py",
        "tests/rhvh41/test_common_subscription.py",
        "tests/rhvh41/test_he_install.py",
        "tests/rhvh41/test_he_info.py",
        "tests/rhvh41/test_vm_registerd.py",
        "tests/rhvh41/test_he_info_add_host.py"]
}

#
# RHVH4.1 test scenarios which has dependency scenario
#

rhvh41_he_install_redeploy = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": "dell-op790-01.qe.lab.eng.nay.redhat.com",
    "DEPEND_SCEN": ["rhvh41_he_install"],
    "CASES": ["tests/rhvh41/test_he_install_redeploy.py"]
}


rhvh41_he_info = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": ["rhvh41_he_install"],
    "CASES": ["tests/rhvh41/test_he_info.py"]
}


rhvh41_he_info_add_host = {
    "TAG": ["RHVH41", "ANOTHER_HOST"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": ["rhvh41_he_install"],
    "CASES": ["tests/rhvh41/test_he_info_add_host.py"]
}

rhvh41_vm_registerd = {
    "TAG": ["RHVH41"],
    "CONFIG": "tests/rhvh41/conf.py",
    "DEPEND_MACHINE": ["dell-op790-01.qe.lab.eng.nay.redhat.com"],
    "DEPEND_SCEN": [],
    "CASES": ["tests/rhvh41/test_vm_registerd.py"]
}
