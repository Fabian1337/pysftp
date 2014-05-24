'''test pysftp.Connection.execute - uses py.test'''

# pylint: disable = W0142
from common import *
from dhp.VI import py_ver


def test_execute_simple_ro():
    '''test execute simple on a read-only server '''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        # always starts at no timeout,
        results = [b'This service allows sftp connections only.\n',]
        assert sftp.execute('ls') == results

@skip_if_ci
def test_execute_simple():
    '''test execute simple'''
    if py_ver() == 2:
        type_check = basestring
    else:
        type_check = str

    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        # always starts at no timeout,
        results = sftp.execute('ls')
        for result in results:
            assert isinstance(result, type_check)

