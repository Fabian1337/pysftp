'''session level fixtures'''
import pytest

from common import SFTP_LOCAL
import pysftp


@pytest.fixture(scope="session")
def lsftp(request):
    '''setup a session long connection to the local sftp server'''
    lsftp = pysftp.Connection(**SFTP_LOCAL)
    request.addfinalizer(lsftp.close)
    return lsftp  # provide the fixture value
