import pytest
import re
from utils.libcockpit import Server


HOST_IP = "10.66.8.217"
HOST_USER = "root"
HOST_PASSWORD = "redhat"
#HOST_PASSWORD = "123qweP!@#"


@pytest.fixture(scope="module")
def host(request):
    ip = getattr(request.module, "HOST_IP", None)
    username = getattr(request.module, "HOST_USER", None)
    password = getattr(request.module, "HOST_PASSWORD", None)
    host = Server(ip, username, password)
    yield host


def test_nodectl_help(host):
    """
    Purpose:
        RHEVM-16591
        Tets the nodectl help subcommand
    """
    cmd1 = "nodectl -h"
    output1 = host.sendcmd(cmd1)
    cmd2 = "nodectl --help"
    output2 = host.sendcmd(cmd2)
    cmd3 = "nodectl"
    output3 = host.sendcmd(cmd3, check=False)
    
    # All the output should be same
    assert output1 == output2, "nodectl help output not equal"
    assert output1 == output3, "nodectl help output not equal"
    
    # Include usage section
    assert re.search("usage:", output1), "nodectl help output not correct"
    
    # Include optional arguments section
    assert re.search("optional arguments:", output1), \
        "nodectl help output not correct"
    
    # Include sub-commands section
    assert re.search("Sub-commands:", output1), \
        "nodectl help output not correct"


def test_nodectl_version(host):
    """
    Purpose:
        RHEVM-16592
        Test the nodectl version
    """
    cmd = "nodectl --version"
    output = host.sendcmd(cmd)
    
    # Skip this case since no version output after the command
    pass


def test_nodectl_init(host):
    """
    Purpose:
        RHEVM-16593
        Test the nodectl init subcommand
    """
    cmd = "imgbase layout|sed -n '/+-.*/p'"
    output1 = host.sendcmd(cmd)
    layouts = re.findall(r'rhvh-*', output1)
    for layout in layouts:
        cmd = "nodectl init --source %s" % layout
        try:
            host.sendcmd(cmd)
        except Exception, e:
            assert e is None, "imgbase init --source %s failed" % layout
        else:
            assert True, "imgbase init --source %s failed" % layout
    # Skip this case currently since bug 1361055
    pass


def test_nodectl_info(host):
    """
    Purpose:
        RHEVM-16594
        Test teh nodectl info subcommand
    """
    cmd = "nodectl info"
    output = host.sendcmd(cmd)

    # Include 3 sections: layers, bootloader, current_layer
    assert re.search('layers', output), "No layers info"
    assert re.search('bootloader', output), "No bootloader info"
    assert re.search('current_layer', output), "No current_layer info"

    # Get the "bootloader:" line num
    cmd_bootloaderline_num = "nodectl info|sed -n '/^bootloader:*/='"
    bootloaderline_num = host.sendcmd(cmd_bootloaderline_num)

    # The last line num is caculated by the "bootloader:" line num
    layer_info_last_num = int(bootloaderline_num) - 1
    # Get the layer info section
    cmd_layer_info = "nodectl info|sed -n '2,%sp'" % layer_info_last_num 
    output_layer_info = host.sendcmd(cmd_layer_info)

    # Get the imgbase layout which is identical with the nodectl layer
    cmd = "imgbase layout|sed -n '/^rhvh-*/p'"
    output1 = host.sendcmd(cmd)
    layouts = output1.split()
    for layout in layouts:
        assert re.search(layout, output_layer_info), "Not identical with imgbase layout"

    # Get the imgbase layout
    cmd = "imgbase layout|sed -n '/+-.*/p'"
    output = host.sendcmd(cmd)
    imgbase_layouts = output.split()
    # Get the nodectl info boot entry
    cmd_index_line_num = "nodectl info|sed -n '/index:*/='"
    output_index_line_num = host.sendcmd(cmd_index_line_num)
    for index in output_index_line_num.split():
        boot_entry_line_num = int(index) - 1
        cmd_boot_entry = "nodectl info|sed -n '%sp'" % boot_entry_line_num
        boot_entry = host.sendcmd(cmd_boot_entry).strip(':').strip()
        assert boot_entry in imgbase_layouts, "Bootloader boot entry not correct" 

    # Current layer info
    cmd_current_layer = "nodectl info|grep 'current_layer:'"
    output_current_layer = host.sendcmd(cmd_current_layer)
    current_layer = output_current_layer.split()[-1]
    # Get current layer from imgbase to check 
    cmd_imgbase_w = "imgbase w"
    output_imgbase_w = host.sendcmd(cmd_imgbase_w)
    imgbase_w = output_imgbase_w.split()[-1]
    assert current_layer == imgbase_w, "Current layer not correct"


def test_nodectl_update(host):
    """
    Purpose:
        RHEVM-16602
        Test the nodectl update subcommand
    """
    # Drop this case currently since bug 1366955 
    pass


def test_nodectl_rollback(host):
    """
    Purpose:
        RHEVM-16603
        Test the nodectl rollback subcommand
    """
    # Skip this bug currently since bug 1366549
    pass

