'''test pysftp.Connection.listdir - uses py.test'''

from io import BytesIO

from common import skip_if_ci, stars8192


def makeflo():
    '''return a proper bytesIO object based on version of py'''
    try:
        flo = BytesIO(stars8192)
    except TypeError:
        flo = BytesIO(bytes(stars8192, 'UTF-8'))
    return flo


@skip_if_ci
def test_truncate_smaller(lsftp):
    '''test truncate, make file smaller'''
    flo = makeflo()
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
    flo = makeflo()
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
    flo = makeflo()
    rname = 'truncate.txt'
    try:
        lsftp.remove(rname)
    except IOError:
        pass
    lsftp.putfo(flo, rname)
    new_size = lsftp.truncate(rname, 8192)
    assert new_size == 8192
    lsftp.remove(rname)


# TODO
# def test_truncate_ro(psftp):
#     '''test truncate, against read-only server'''
#     rname = '/home/test/readme.txt'
#     with pytest.raises(IOError):
#         _ = psftp.truncate(rname, 8192)
