'''test pysftp.Connection.readlink - uses py.test'''
from __future__ import print_function

from common import skip_if_ci
from io import BytesIO


@skip_if_ci
def test_readlink(lsftp):
    '''test the readlink method'''
    rfile = 'readme.txt'
    rlink = 'readme.sym'
    buf = b'I will not buy this record, it is scratched\nMy hovercraft'\
          b' is full of eels.'
    flo = BytesIO(buf)
    print(lsftp.listdir())
    lsftp.putfo(flo, rfile)
    lsftp.symlink(rfile, rlink)

    assert lsftp.readlink(rlink) == '/home/test/readme.txt'
    lsftp.remove(rlink)
    lsftp.remove(rfile)
