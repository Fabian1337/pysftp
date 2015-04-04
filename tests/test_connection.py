'''test pysftp.Connection - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_connection_with(sftpserver):
    '''connect to a public sftp server'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            assert psftp.listdir() == [u'pub', u'read.me']


def test_connection_bad_host():
    '''attempt connection to a non-existing server'''
    with pytest.raises(pysftp.ConnectionException):
        sftp = pysftp.Connection(host='',
                                 username='demo',
                                 password='password')
        sftp.close()


@skip_if_ci
def test_connection_bad_credentials(lsftp):
    '''attempt connection to a non-existing server'''
    copts = SFTP_LOCAL.copy()
    copts['password'] = 'badword'
    with pytest.raises(pysftp.SSHException):
        with pysftp.Connection(**copts) as sftp:
            pass


def test_connection_good(sftpserver):
    '''connect to a public sftp server'''
    with sftpserver.serve_content(CONTENT):
        sftp = pysftp.Connection(**conn(sftpserver))
        sftp.close()
