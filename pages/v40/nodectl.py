import re
import simplejson
from fabric.api import run, settings


class Nodectl():

    def check_nodectl_help(self):
        """
        Purpose:
            RHEVM-16591
            Tets the nodectl help subcommand
        """
        cmd1 = "nodectl -h"
        output1 = run(cmd1)
        cmd2 = "nodectl --help"
        output2 = run(cmd2)
        cmd3 = "nodectl"
        with settings(warn_only=True):
            output3 = run(cmd3)

        # All the output should be same
        assert output1 == output2, "nodectl help output not equal"
        assert output1 == output3, "nodectl help output not equal"

        # Include usage section
        assert re.search("usage:", output1), "nodectl help not correct"

        # Include optional arguments section
        assert re.search("optional arguments:", output1), \
            "nodectl help not correct"

        # Include sub-commands section
        assert re.search("Sub-commands:", output1), "nodectl help not correct"

    def check_nodectl_version(self):
        """
        Purpose:
            RHEVM-16592
            Test the nodectl version
        """
        cmd = "nodectl --version"
        run(cmd)

        # Skip this case since no version were output
        raise NotImplementedError

    def check_nodectl_init(self):
        """
        Purpose:
            RHEVM-16593
            Test the nodectl init subcommand
        """
        # Skip this case currently since bug 1361055
        raise NotImplementedError

    def check_nodectl_info(self, layer):
        """
        Purpose:
            RHEVM-16594
            Test teh nodectl info subcommand
        """
        cmd_info = "nodectl info --machine-readable"
        output_info = run(cmd_info)
        info_dict = simplejson.loads(output_info)

        # Check layers
        assert 'layers' in info_dict.keys(), "nodectl info not correct"
        assert layer in info_dict['layers'].keys(), "nodectl info not correct"

        # Check bootloader
        assert 'bootloader' in info_dict.keys(), "nodectl info not correct"
        entry = layer + "+1"
        assert info_dict['bootloader']['default'] == entry, \
            "nodectl info not correct"

        # Check current layer
        assert 'current_layer' in info_dict.keys()
        assert entry == info_dict['current_layer'], "nodectl info not correct"

        # Check "nodectl info" return 0
        cmd_info = "nodectl info"
        run(cmd_info)

    def check_nodectl_update(self):
        """
        Purpose:
            RHEVM-16602
            Test the nodectl update subcommand
        """
        # Drop this case currently since bug 1366955
        raise NotImplementedError

    def check_nodectl_rollback(self):
        """
        Purpose:
            RHEVM-16603
            Test the nodectl rollback subcommand
        """
        # Skip this case currently since bug 1366549
        raise NotImplementedError

    def check_nodectl_check(self):
        """
        Purpose:
            RHEVM-16604
            Test the nodectl check subcommand
        """
        cmd_check = "nodectl check --machine-readable"
        check_info = run(cmd_check)
        check_info_dict = simplejson.loads(check_info)

        # Get the check status
        nodectl_check_status = check_info_dict['status']
        print nodectl_check_status

        # Get the mounts status
        mount_points_status = check_info_dict['mount_points']['status']

        # Get the basic storage status
        basic_storage_status = check_info_dict['basic_storage']['status']

        # Get the vdsmd status
        vdsmd_status = check_info_dict['vdsmd']['status']

        # Get the vdsmd service status
        cmd_sys_vdsmd_status = "systemctl status vdsmd.service|grep Active"
        output_sys_vdsmd_status = run(cmd_sys_vdsmd_status)
        sys_vdsmd_status = output_sys_vdsmd_status.split()[1]

        # If vdsmd running, vdsmd check should be 'OK'
        if sys_vdsmd_status == "active":
            assert nodectl_check_status == 'ok', "nodectl check status: bad"
            assert vdsmd_status == 'ok', "nodectl check vdsmd: bad"
        else:
            assert mount_points_status == 'ok', \
                "nodectl check mount points: bad"
            assert basic_storage_status == 'ok', \
                "nodectl check basci storage: bad"

    def check_nodectl_debug(self):
        """
        Purpose:
            RHEVM-16605
            Test the nodectl sub-command --debug
        """
        # nodectl info debug
        cmd_info = "nodectl info --debug"
        run(cmd_info)

        # nodectl update --debug
        # cmd_update = "nodectl update --debug"
        # run(cmd_update)

        # nodectl rollback --debug
        # cmd_rollback = "nodectl rollback --debug"
        # run(cmd_rollback)

        # nodectl check --debug
        cmd_check = "nodectl check --debug"
        run(cmd_check)

        # nodectl init --debug
        cmd = "imgbase layout|sed -n '/+-.*/p'"
        output1 = run(cmd)
        layouts = re.findall(r'rhvh-.*', output1)
        for layout in layouts:
            cmd = "nodectl init --source %s --debug" % layout
            run(cmd)

    def check_nodectl_json(self):
        """
        Purpose:
            RHEVM-16606
            Test the nodectl sub-command --machine-readable
        """
        # nodectl info --machine-readable
        cmd_nodectl_info = "nodectl info --machine-readable"
        output_nodectl_info = run(cmd_nodectl_info)
        nodectl_info_dict = simplejson.loads(output_nodectl_info)
        assert nodectl_info_dict, "nodectl json output failed"

        # nodectl info --machine-readable
        cmd_nodectl_check = "nodectl check --machine-readable"
        output_nodectl_check = run(cmd_nodectl_check)
        nodectl_check_dict = simplejson.loads(output_nodectl_check)
        assert nodectl_check_dict, "nodectl json output failed"
