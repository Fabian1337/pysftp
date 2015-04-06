'''test pysftp.Connection.stat and .lstat - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_stat(sftpserver):
    '''test stat'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            dirname = 'pub'
            rslt = sftp.stat(dirname)
            assert rslt.st_size >= 0


@skip_if_ci
def test_lstat(lsftp):
    '''test lstat  minimal, have to use real server, plugin doesn't support
    lstat'''
    dirname = 'pub'
    lsftp.mkdir(dirname)
    lsftp.chdir('/home/test')
    rslt = lsftp.lstat(dirname)
    lsftp.rmdir(dirname)
    assert rslt.st_size >= 0
