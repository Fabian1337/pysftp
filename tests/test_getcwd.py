'''test pysftp.Connection.rename - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_getcwd_none():
    '''test .getcwd as the first operation - need pristine connection'''
    sftp = pysftp.Connection(**SFTP_PUBLIC)
    assert sftp.getcwd() is None


def test_getcwd_after_chdir(psftp):
    '''test getcwd after a chdir operation'''
    psftp.chdir('/home/test/pub')
    assert psftp.getcwd() == '/home/test/pub'
