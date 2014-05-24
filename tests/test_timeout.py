'''test pysftp.Connection.timeout - uses py.test'''

# pylint: disable = W0142
from common import *


def test_timeout_getter():
    '''test getting the timeout value'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        # always starts at no timeout,
        assert sftp.timeout is None


def test_timeout_setter():
    '''test setting the timeout value'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.timeout = 10.5
        assert sftp.timeout == 10.5
        sftp.timeout = None
        assert sftp.timeout is None
