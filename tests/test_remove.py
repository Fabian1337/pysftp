'''test remove and unlink methods - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


@skip_if_ci
def test_remove():
    '''test the remove method'''
    with tempfile_containing('*'* 8192) as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            sftp.put(fname)
            is_there = base_fname in sftp.listdir()
            sftp.remove(base_fname)
            not_there = base_fname not in sftp.listdir()

    assert is_there
    assert not_there

@skip_if_ci
def test_unlink():
    '''test the unlink function'''
    with tempfile_containing('*'* 8192) as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            sftp.put(fname)
            is_there = base_fname in sftp.listdir()
            sftp.unlink(base_fname)
            not_there = base_fname not in sftp.listdir()

    assert is_there
    assert not_there

def test_remove_roserver():
    '''test reaction of attempting remove on read-only server'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with pytest.raises(IOError):
            sftp.remove('readme.txt')

@skip_if_ci
def test_remove_does_not_exist():
    '''test remove against a non-existant file'''
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        with pytest.raises(IOError):
            sftp.remove('i-am-not-here.txt')
