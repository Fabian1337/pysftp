'''test pysftp.Connection.open - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}


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
