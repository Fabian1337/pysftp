'''test pysftp.Connection.normalize - uses py.test'''

# pylint: disable = W0142
from common import *


def test_normalize(sftpserver):
    '''test the normalize function'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.chdir('/')
            assert psftp.normalize('make.txt') == '/make.txt'
            assert psftp.normalize('.') == '/'
            assert psftp.normalize('pub') == '/pub'
            psftp.chdir('pub')
            assert psftp.normalize('.') == '/pub'


# TODO
# def test_normalize_symlink(psftp):
#     '''test normalize against a symlink'''
#     psftp.chdir('/home/test')
#     rsym = 'readme.sym'
#     assert psftp.normalize(rsym) == '/home/test/readme.txt'


def test_pwd(sftpserver):
    '''test the pwd property'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.chdir('/pub/foo2')
            assert psftp.pwd == '/pub/foo2'
            psftp.chdir('bar1')
            assert psftp.pwd == '/pub/foo2/bar1'
            psftp.chdir('../../foo1')
            assert psftp.pwd == '/pub/foo1'
