'''test pysftp.Connection.readlink - uses py.test'''

# pylint: disable = W0142
from common import *


def test_readlink(psftp):
    '''test the readlink method'''
    assert psftp.readlink('readme.sym') == '/home/test/readme.txt'
