'''test pysftp.Connection.timeout - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp


# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}


def test_timeout_getter():
    '''test getting the timeout value '.' '''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        # always starts at no timeout,
        assert sftp.timeout is None


def test_timeout_setter():
    '''test setting the timeout value '.' '''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.timeout = 10.5
        assert sftp.timeout == 10.5
        sftp.timeout = None
        assert sftp.timeout is None
