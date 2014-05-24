'''test pysftp.Connection.listdir - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from io import BytesIO

@skip_if_ci
def test_truncate_smaller():
    '''test truncate, make file smaller'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        try:
            sftp.remove(rname)
        except IOError:
            pass
        sftp.putfo(flo, rname)
        new_size = sftp.truncate(rname, 4096)
        assert new_size == 4096
        sftp.remove(rname)

@skip_if_ci
def test_truncate_larger():
    '''test truncate, make file larger'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        try:
            sftp.remove(rname)
        except IOError:
            pass
        sftp.putfo(flo, rname)
        new_size = sftp.truncate(rname, 2*8192)
        assert new_size == 2*8192
        sftp.remove(rname)

@skip_if_ci
def test_truncate_same():
    '''test truncate, make file same size'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        try:
            sftp.remove(rname)
        except IOError:
            pass
        sftp.putfo(flo, rname)
        new_size = sftp.truncate(rname, 8192)
        assert new_size == 8192
        sftp.remove(rname)

def test_truncate_ro():
    '''test truncate, against read-only server'''
    rname = 'readme.txt'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with pytest.raises(IOError):
            _ = sftp.truncate(rname, 8192)

