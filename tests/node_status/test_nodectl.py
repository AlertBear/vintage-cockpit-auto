from fabric.api import env
import pytest
from pages.nodectl import Nodectl

env.host_string = 'root@10.66.8.217'
env.password = 'redhat'
test_layer = 'rhvh-4.0-0.20160919.0'


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
    nodectl.check_nodectl_info(test_layer)


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
