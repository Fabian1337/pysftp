'''test pysftp.Connection.listdir - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from io import BytesIO


@skip_if_ci
def test_truncate_smaller(lsftp):
    '''test truncate, make file smaller'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    try:
        lsftp.remove(rname)
    except IOError:
        pass
    lsftp.putfo(flo, rname)
    new_size = lsftp.truncate(rname, 4096)
    assert new_size == 4096
    lsftp.remove(rname)


@skip_if_ci
def test_truncate_larger(lsftp):
    '''test truncate, make file larger'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    try:
        lsftp.remove(rname)
    except IOError:
        pass
    lsftp.putfo(flo, rname)
    new_size = lsftp.truncate(rname, 2*8192)
    assert new_size == 2*8192
    lsftp.remove(rname)


@skip_if_ci
def test_truncate_same(lsftp):
    '''test truncate, make file same size'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    try:
        lsftp.remove(rname)
    except IOError:
        pass
    lsftp.putfo(flo, rname)
    new_size = lsftp.truncate(rname, 8192)
    assert new_size == 8192
    lsftp.remove(rname)


def test_truncate_ro(psftp):
    '''test truncate, against read-only server'''
    rname = '/home/test/readme.txt'
    with pytest.raises(IOError):
        _ = psftp.truncate(rname, 8192)
