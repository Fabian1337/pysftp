'''session level fixtures'''
from common import *
import pytest

@pytest.fixture(scope="session")
def psftp(request):
    psftp = pysftp.Connection(**SFTP_PUBLIC)
    request.addfinalizer(psftp.close)
    return psftp  # provide the fixture value

@pytest.fixture(scope="session")
def lsftp(request):
    lsftp = pysftp.Connection(**SFTP_LOCAL)
    request.addfinalizer(lsftp.close)
    return lsftp  # provide the fixture value
