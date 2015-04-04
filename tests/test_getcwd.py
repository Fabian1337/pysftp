'''test pysftp.Connection.rename - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_getcwd_none(sftpserver):
    '''test .getcwd as the first operation - need pristine connection'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            assert psftp.getcwd() is None


def test_getcwd_after_chdir(sftpserver):
    '''test getcwd after a chdir operation'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.chdir('/pub/foo1')
            assert psftp.getcwd() == '/pub/foo1'
