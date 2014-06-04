'''session level fixtures'''
from common import *
import pytest

# pylint: disable=E1101
# pylint: disable = W0142,W0621


@pytest.fixture(scope="session")
def psftp(request):
    '''setup a session long connection to the public read-only sftp server'''
    psftp = pysftp.Connection(**SFTP_PUBLIC)
    request.addfinalizer(psftp.close)
    return psftp  # provide the fixture value


@pytest.fixture(scope="session")
def lsftp(request):
    '''setup a session long connection to the local sftp server'''
    lsftp = pysftp.Connection(**SFTP_LOCAL)
    request.addfinalizer(lsftp.close)
    return lsftp  # provide the fixture value
