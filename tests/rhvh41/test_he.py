import pytest
from pages.he_info import HeInfo
from fabric.api import env
from utils.helpers import Config

cfg = Config('./cockpit.ini')

host_ip = cfg.get('SHARE', 'HOST_IP')
host_user = cfg.get('SHARE', 'HOST_USER')
host_password = cfg.get('SHARE', 'HOST_PASSWORD')

env.host_string = host_user + '@' + host_ip
env.password = host_password


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
