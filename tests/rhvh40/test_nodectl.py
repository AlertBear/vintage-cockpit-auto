from fabric.api import env
import pytest
from pages.rhvh40.nodectl import Nodectl
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


def test_16591(firefox):
    """
    Purpose:
        RHEVM-16591
        Tets the nodectl help subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_help()


def test_16594(firefox):
    """
    Purpose:
        RHEVM-16594
        Test teh nodectl info subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_info(test_build)


def test_16604(firefox):
    """
    Purpose:
        RHEVM-16604
        Test the nodectl check subcommand
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_check()


def test_16605(firefox):
    """
    Purpose:
        RHEVM-16605
        Test the nodectl sub-command --debug
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_debug()


def test_16606(firefox):
    """
    Purpose:
        RHEVM-16606
        Test the nodectl sub-command --machine-readable
    """
    nodectl = Nodectl()
    nodectl.check_nodectl_json()
