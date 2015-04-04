'''test pysftp.Connection.open - uses py.test'''

# pylint: disable = W0142
from common import *


def test_open_read(sftpserver):
    '''test the open function'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.chdir('/pub')
            rfile = psftp.open('make.txt')
            contents = rfile.read()
            rfile.close()
            assert contents == b'content of make.txt'


def test_open_read_with(sftpserver):
    '''test the open function in a with statment'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.chdir('/pub')
            with psftp.open('make.txt') as rfile:
                contents = rfile.read()
            assert contents == b'content of make.txt'
