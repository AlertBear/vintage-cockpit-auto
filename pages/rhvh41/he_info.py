from fabric.api import run


class HeInfo():

    def check_he_info(self):
        """
        Purpose:
            RHEVM-16340:Verify HE via non-default cockpit port
        """
        cmd1 = "systemctl status cockpit |grep 'Active' |awk -F ' ' '{print $2}'"
        output1 = run(cmd1)
        cmd2 = "systemctl status cockpit |grep 'Active' |awk -F ' ' '{print $3}'"
        output2 = run(cmd2)
        cmd3 = "cockpit-bridge --packages"
        output3 = run(cmd3)

        assert output1 == "active", "Cockpit status is not active"
        assert output2 == "(running)", "Cockpit is not running"
        assert output3, "packages are not exists"
