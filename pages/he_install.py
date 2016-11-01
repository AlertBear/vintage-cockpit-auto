import time
from selenium import webdriver
from fabric.api import run, settings, put
import logging
from vncdotool import api


def press_keys(seq, cli):
    """press keys sequence

    """
    for keys in seq:
        if len(keys) > 1:
            for k in keys:
                cli.keyPress(k)
                time.sleep(0.5)
        elif len(keys) == 1:
            cli.keyPress("shift-%s" % keys[0])
        else:
            logging.warning("Error at least should have one key")


class HandleVNCSetup:

    def __init__(self, host_ip, host_password, vnc_password='redhat'):
        self.host_ip = host_ip
        self.host_password = host_password
        self.vnc_password = vnc_password
        self._set_vnc_pass()
        self.cli = api.connect(self.ip, password=self.vnc_pass)

    def _set_vnc_pass(self):
        with settings(warn_only=True, host_string='root@' + self.ip, password=self.host_password):
            run('hosted-engine --add-console-password --password=%s' % self.vnc_password, quiet=True)

    def turn_on_ssh(self):
        for k in 'root':
            self.cli.keyPress(k)
            time.sleep(0.1)
        self.cli.keyPress('enter')
        time.sleep(1)

        for k in 'redhat':
            self.cli.keyPress(k)
            time.sleep(0.1)
        self.cli.keyPress('enter')
        time.sleep(1)

        #############################################
        for k in "sed -i 's/":
            self.cli.keyPress(k)
            time.sleep(0.1)

        self.cli.keyPress('shift-3')  # --> '#'

        for k in "PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd":
            self.cli.keyPress(k)
            time.sleep(0.1)

        self.cli.keyPress('shift-_')  # --> '_'

        for k in "config":
            self.cli.keyPress(k)
            time.sleep(0.1)

        time.sleep(1)
        self.cli.keyPress('enter')
        time.sleep(1)

        #####################################

        for k in "sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd":
            self.cli.keyPress(k)
            time.sleep(0.1)

        self.cli.keyPress('shift-_')  # --> '_'

        for k in "config":
            self.cli.keyPress(k)
            time.sleep(0.1)

        time.sleep(1)
        self.cli.keyPress('enter')
        time.sleep(1)

        ##################################

        for k in "service sshd restart":
            self.cli.keyPress(k)
            time.sleep(0.1)
        time.sleep(1)
        self.cli.keyPress('enter')
        time.sleep(1)

        logging.warning("Hope ssh is turn on, cause is hard to see if success.")


def he_install(host_dict, nfs_dict, install_dict, vm_dict):
    host_ip = host_dict['host_ip']
    root_uri = "https://" + host_ip + ":9090"
    host_user = host_dict['host_user']
    host_password = host_dict['host_password']
    nfs_ip = nfs_dict['nfs_ip']
    nfs_password = nfs_dict['nfs_password']
    nfs_path = nfs_dict['nfs_path']
    ova_path = install_dict['ova_path']
    nic = install_dict['nic']
    deploy_mode = install_dict['deploy_mode']
    storage_path = install_dict['storage_path']
    mac = install_dict['mac']
    vm_fqdn = vm_dict['vm_fqdn']
    vm_ip = vm_dict['vm_ip']
    vm_password = vm_dict['vm_password']
    engine_password = vm_dict['engine_password']
    auto_answer = vm_dict['auto_answer']

    with settings(warn_only=True, host_string='root@' + nfs_ip, password=nfs_password):
        run("rm -rf %s/*" % nfs_path)
        run("service nfs start",quiet=True)

    with settings(warn_only=True, host_string='root@' + host_ip, password=host_password):
        cmd0 = "hostname"
        host_name = run(cmd0)
        cmd1 = "echo '%s  %s' >> /etc/hosts" % (host_ip, host_name)
        run(cmd1)
        cmd2 = "echo '%s  %s' >> /etc/hosts" % (vm_ip, vm_fqdn)
        run(cmd2)
        put(ova_path, "/opt/%s" % ova_path.split('/')[-1])

    time.sleep(1)
    dr = webdriver.Firefox()
    dr.get(root_uri)
    time.sleep(5)
    id = dr.find_element_by_id
    class_name = dr.find_element_by_class_name
    xpath = dr.find_element_by_xpath

    id("login-user-input").send_keys("root")
    time.sleep(1)
    id("login-password-input").send_keys("redhat")
    time.sleep(1)
    id("login-button").click()
    time.sleep(5)
    dr.get(root_uri + "/ovirt-dashboard")
    dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
    xpath("//a[@href='#/he']").click()
    time.sleep(3)
    class_name("btn-primary").click()
    time.sleep(5)
    class_name("btn-default").click()    # click next button,continue yes
    time.sleep(35)
    class_name("btn-default").click()    # use storage model
    time.sleep(2)
    nfs_storage = nfs_ip + ':' + nfs_path
    class_name("form-control").send_keys(nfs_storage)  # NFS storage path
    time.sleep(2)
    class_name("btn-default").click()    # confirm nfs storage path
    time.sleep(5)
    class_name("btn-default").click()    # iptables default confirm
    time.sleep(2)
    class_name("btn-default").click()    # gateway ip confirm
    time.sleep(2)
    class_name("form-control").clear()   # select NIC
    time.sleep(1)
    class_name("form-control").send_keys(nic)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()   # select deploy model
    time.sleep(1)
    class_name("form-control").send_keys(deploy_mode)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()    # select vnc
    time.sleep(1)
    class_name("form-control").clear()   # input ova path
    time.sleep(1)
    class_name("form-control").send_keys("/opt/%s" % ova_path.split('/')[-1])
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(65)

    class_name("form-control").clear()
    time.sleep(2)
    class_name("form-control").send_keys(storage_path)
    time.sleep(5)
    class_name("btn-default").click()
    time.sleep(3)

    class_name("btn-default").click()    # select cloud-init
    time.sleep(2)
    class_name("btn-default").click()    # select Generate
    time.sleep(2)
    class_name("form-control").send_keys(vm_fqdn)  # set VM FQDN
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()      # Manual setup
    time.sleep(1)
    class_name("form-control").send_keys("no")
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()       # Set VM domain
    time.sleep(2)
    class_name("form-control").clear()      # set root password
    time.sleep(1)
    class_name("form-control").send_keys(vm_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()
    time.sleep(1)
    class_name("form-control").send_keys(vm_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()     # set cpu type,default
    time.sleep(2)
    class_name("btn-default").click()     # set the number of vcpu
    time.sleep(2)
    class_name("form-control").clear()    # set unicast MAC
    time.sleep(1)
    class_name("form-control").send_keys(mac)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()    # set memory size
    time.sleep(1)
    class_name("form-control").send_keys("4096")
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()     # network,default DHCP
    time.sleep(2)
    class_name("btn-default").click()     # resovle hostname
    time.sleep(2)
    class_name("form-control").clear()    # set engine admin password
    time.sleep(1)
    class_name("form-control").send_keys(engine_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(1)
    class_name("form-control").clear()
    time.sleep(1)
    class_name("form-control").send_keys(engine_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()    # set hostname, default hosted_engine_x
    time.sleep(2)
    class_name("btn-default").click()    # set the name of SMTP
    time.sleep(1)
    class_name("btn-default").click()    # set the port of SMTP,default 25
    time.sleep(1)
    class_name("btn-default").click()    # set email address
    time.sleep(1)
    class_name("btn-default").click()    # set comma-separated email address
    time.sleep(5)
    class_name("btn-default").click()    # confirm the configuration
    time.sleep(600)

    with settings(warn_only=True, host_string='root@' + host_ip, password=host_password):
        HandleVNCSetup(host_ip=self.host_ip, host_password=host_password).turn_on_ssh()
    time.sleep(10)

    with settings(warn_only=True, host_string='root@' + vm_ip, password=vm_password):
        put(auto_answer, "/root/run")
        run("chmod 755 /root/run")
        run("/root/run -i")
    time.sleep(40)

    class_name("btn-default").click()
    time.sleep(500)

    with settings(warn_only=True, host_string='root@' + vm_ip, password=vm_password):
        run("reboot", quiet=True)
    time.sleep(60)
