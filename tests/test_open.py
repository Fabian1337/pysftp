'''test pysftp.Connection.open - uses py.test'''

# pylint: disable = W0142
from common import *

def test_open_read():
    '''test the open function'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        rfile = sftp.open('readme.txt')
        contents = rfile.read()
        rfile.close()
    assert contents[0:9] == b'This SFTP'

def test_open_read_with():
    '''test the open function in a with statment'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with sftp.open('readme.txt') as rfile:
            contents = rfile.read()
    assert contents[0:9] == b'This SFTP'
