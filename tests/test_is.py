'''test pysftp.Connection.isX methods - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_isfile(sftpserver):
    '''test .isfile() functionality'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            rfile = '/pub/make.txt'
            rdir = 'pub'
            assert psftp.isfile(rfile)
            assert psftp.isfile(rdir) is False


# TODO
# def test_isfile_2(psftp):
#     '''test .isfile() functionality against a symlink'''
#     rsym = '/home/test/readme.sym'
#     assert psftp.isfile(rsym)


def test_isdir(sftpserver):
    '''test .isdir() functionality'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            rfile = '/pub/make.txt'
            rdir = '/pub'
            assert psftp.isdir(rfile) is False
            assert psftp.isdir(rdir)


# TODO
# def test_isdir_2(psftp):
#     '''test .isdir() functionality against a symlink'''
#     rsym = '/home/test/readme.sym'
#     assert psftp.isdir(rsym) is False
