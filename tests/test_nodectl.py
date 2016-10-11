from fabric.api import env
import pytest
from pages.nodectl import Nodectl
from conf import *


host_ip = HOST_IP
host_username = HOST_CREDENTIAL[0]
host_password = HOST_CREDENTIAL[1]
env.host_string = host_username + '@' + host_ip
env.password = host_password
test_build = BUILD_VERSION


@pytest.fixture(scope="module")
def firefox(request):
    pass


def test_nodectl_help(firefox):
    """
    Purpose:
        RHEVM-16591
        Tets the nodectl help subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_help()


def test_nodectl_info(firefox):
    """
    Purpose:
        RHEVM-16594
        Test teh nodectl info subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_info(test_build)


def test_nodectl_check(firefox):
    """
    Purpose:
        RHEVM-16604
        Test the nodectl check subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_check()


def test_nodectl_debug(firefox):
    """
    Purpose:
        RHEVM-16605
        Test the nodectl sub-command --debug
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_debug()


def test_nodectl_json(firefox):
    """
    Purpose:
        RHEVM-16606
        Test the nodectl sub-command --machine-readable
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_json()
