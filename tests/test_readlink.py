'''test pysftp.Connection.readlink - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp


# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}

def test_readlink():
    '''test the readlink method'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.readlink('readme.sym') == '/home/test/readme.txt'
