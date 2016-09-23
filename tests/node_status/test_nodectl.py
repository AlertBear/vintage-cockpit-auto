from fabric.api import env
import pytest
from pages.nodectl import Nodectl

env.host_string = 'root@10.66.8.217'
env.password = 'redhat'


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
