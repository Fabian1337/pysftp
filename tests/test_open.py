'''test pysftp.Connection.open - uses py.test'''

# pylint: disable = W0142
from common import *


def test_open_read(psftp):
    '''test the open function'''
    psftp.chdir('/home/test')
    rfile = psftp.open('readme.txt')
    contents = rfile.read()
    rfile.close()
    assert contents[0:9] == b'This SFTP'


def test_open_read_with(psftp):
    '''test the open function in a with statment'''
    psftp.chdir('/home/test')
    with psftp.open('readme.txt') as rfile:
        contents = rfile.read()
    assert contents[0:9] == b'This SFTP'
