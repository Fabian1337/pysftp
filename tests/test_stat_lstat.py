'''test pysftp.Connection.stat and .lstat - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_stat(sftpserver):
    '''test stat'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            dirname = 'pub'
            sftp.chdir('/')
            rslt = sftp.stat(dirname)
            assert rslt.st_size >= 0


@skip_if_ci
def test_lstat(lsftp):
    '''test lstat  minimal'''
    dirname = 'pub'
    lsftp.mkdir(dirname)
    lsftp.chdir('/home/test')
    rslt = lsftp.lstat(dirname)
    lsftp.rmdir(dirname)
    assert rslt.st_size >= 0
