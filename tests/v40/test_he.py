import pytest
from pages.rhvh40.he_info import HeInfo
from fabric.api import env
from conf import *


env.host_string = 'root@' + HOST_IP
env.password = HOST_CREDENTIAL[-1]


@pytest.fixture(scope="module")
def firefox(request):
    pass


def test_16340(firefox):
    """
    Purpose:
        RHEVM-16340
        Tests the HE_info
    """
    he_info = HeInfo()
    he_info.check_he_info()
