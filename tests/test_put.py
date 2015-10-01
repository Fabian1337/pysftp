'''test pysftp.Connection.put - uses py.test'''

import os
from time import sleep

from dhp.test import tempfile_containing
from mock import Mock
import pytest

from common import VFS, conn, skip_if_ci, stars8192
import pysftp


@skip_if_ci
def test_put_callback(lsftp):
    '''test the callback feature of put'''
    cback = Mock(return_value=None)
    with tempfile_containing(contents=4096*'*') as fname:
        base_fname = os.path.split(fname)[1]
        lsftp.chdir('/home/test')
        lsftp.put(fname, callback=cback)
        # clean up
        lsftp.remove(base_fname)
    # verify callback was called more than once - usually a min of 2
    assert cback.call_count >= 2


@skip_if_ci
def test_put_confirm(lsftp):
    '''test the confirm feature of put'''
    with tempfile_containing(contents=8192*'*') as fname:
        base_fname = os.path.split(fname)[1]
        lsftp.chdir('/home/test')
        result = lsftp.put(fname)
        # clean up
        lsftp.remove(base_fname)
    # verify that an SFTPAttribute like os.stat was returned
    assert result.st_size == 8192
    assert result.st_uid is not None
    assert result.st_gid is not None
    assert result.st_atime
    assert result.st_mtime


@skip_if_ci
def test_put(lsftp):
    '''run test on localhost'''
    contents = 'now is the time\nfor all good...'
    with tempfile_containing(contents=contents) as fname:
        base_fname = os.path.split(fname)[1]
        if base_fname in lsftp.listdir():
            lsftp.remove(base_fname)
        assert base_fname not in lsftp.listdir()
        lsftp.put(fname)
        assert base_fname in lsftp.listdir()
        with tempfile_containing('') as tfile:
            lsftp.get(base_fname, tfile)
            assert open(tfile).read() == contents
        # clean up
        lsftp.remove(base_fname)


def test_put_bad_local(sftpserver):
    '''try to put a non-existing file to a read-only server'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            with tempfile_containing('should fail') as fname:
                pass
            # tempfile has been removed
            with pytest.raises(OSError):
                sftp.put(fname)


# TODO
# def test_put_not_allowed(psftp):
#     '''try to put a file to a read-only server'''
#     with tempfile_containing('should fail') as fname:
#         with pytest.raises(IOError):
#             psftp.put(fname)


@skip_if_ci
def test_put_preserve_mtime(lsftp):
    '''test that m_time is preserved from local to remote, when put'''
    with tempfile_containing(contents=stars8192) as fname:
        base_fname = os.path.split(fname)[1]
        base = os.stat(fname)
        # with pysftp.Connection(**SFTP_LOCAL) as sftp:
        result1 = lsftp.put(fname, preserve_mtime=True)
        sleep(2)
        result2 = lsftp.put(fname, preserve_mtime=True)
        # clean up
        lsftp.remove(base_fname)
    # see if times are modified
    # assert base.st_atime == result1.st_atime
    assert int(base.st_mtime) == result1.st_mtime
    # assert result1.st_atime == result2.st_atime
    assert int(result1.st_mtime) == result2.st_mtime
