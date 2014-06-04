'''test pysftp.Connection.listdir - uses py.test'''

# pylint: disable = W0142
from common import *


def test_listdir(psftp):
    '''test listdir'''
    psftp.cwd('/home/test')
    assert psftp.listdir() == ['pub', 'readme.sym', 'readme.txt']


def test_listdir_attr(psftp):
    '''test listdir'''
    psftp.cwd('/home/test')
    attrs = psftp.listdir_attr()
    assert len(attrs) == 3
    # test they are in filename order
    assert attrs[0].filename == 'pub'
    assert attrs[1].filename == 'readme.sym'
    assert attrs[2].filename == 'readme.txt'
    # test that longname is there
    for attr in attrs:
        assert attr.longname is not None
