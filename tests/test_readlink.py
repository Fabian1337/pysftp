'''test pysftp.Connection.readlink - uses py.test'''

# pylint: disable = W0142
from common import *


def test_readlink():
    '''test the readlink method'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.readlink('readme.sym') == '/home/test/readme.txt'
