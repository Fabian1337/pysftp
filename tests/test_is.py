'''test pysftp.Connection.isX methods - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_isfile(sftpserver):
    '''test .isfile() functionality'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            rfile = 'pub/make.txt'
            rdir = 'pub'
            assert sftp.isfile(rfile)
            assert sftp.isfile(rdir) is False


# TODO
# def test_isfile_2(sftp):
#     '''test .isfile() functionality against a symlink'''
#     rsym = '/home/test/readme.sym'
#     assert sftp.isfile(rsym)


def test_isdir(sftpserver):
    '''test .isdir() functionality'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            rfile = 'pub/make.txt'
            rdir = 'pub'
            assert sftp.isdir(rfile) is False
            assert sftp.isdir(rdir)


# TODO
# def test_isdir_2(sftp):
#     '''test .isdir() functionality against a symlink'''
#     rsym = '/home/test/readme.sym'
#     assert sftp.isdir(rsym) is False
