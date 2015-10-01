'''test pysftp.Connection.walktree and pysftp.walktree - uses py.test'''
from __future__ import print_function

from mock import Mock, call
import pytest

from common import VFS, conn
import pysftp


def test_walktree_cbclass(sftpserver):
    '''test the walktree function with callbacks from a class'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            wtcb = pysftp.WTCallbacks()
            sftp.walktree('.',
                          fcallback=wtcb.file_cb,
                          dcallback=wtcb.dir_cb,
                          ucallback=wtcb.unk_cb)

            assert './pub/foo2/bar1/bar1.txt' in wtcb.flist
            assert './read.me' in wtcb.flist
            assert len(wtcb.flist) > 3

            dlist = ['./pub', './pub/foo1', './pub/foo2',
                     './pub/foo2/bar1']
            assert wtcb.dlist == dlist

            assert wtcb.ulist == []


def test_walktree_cbmock(sftpserver):
    '''test the walktree function, with mocked callbacks (standalone functions)
    '''
    file_cb = Mock(return_value=None)
    dir_cb = Mock(return_value=None)
    unk_cb = Mock(return_value=None)

    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            sftp.walktree('.',
                          fcallback=file_cb,
                          dcallback=dir_cb,
                          ucallback=unk_cb)
            # check calls to the file callback
            file_cb.assert_called_with('./read.me')
            thecall = call('./pub/foo2/bar1/bar1.txt')
            assert thecall in file_cb.mock_calls
            assert file_cb.call_count > 3
            # check calls to the directory callback
            assert [call('./pub'),
                    call('./pub/foo1'),
                    call('./pub/foo2'),
                    call('./pub/foo2/bar1')] == dir_cb.mock_calls
            # check calls to the unknown callback
            assert [] == unk_cb.mock_calls


def test_walktree_no_recurse(sftpserver):
    '''test the walktree function, with mocked callbacks (standalone functions)
    '''
    file_cb = Mock(return_value=None)
    dir_cb = Mock(return_value=None)
    unk_cb = Mock(return_value=None)

    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            sftp.walktree('.',
                          fcallback=file_cb,
                          dcallback=dir_cb,
                          ucallback=unk_cb,
                          recurse=False)
            # check calls to the file callback
            thecall = call('./read.me')
            assert thecall in file_cb.mock_calls
            assert file_cb.call_count == 1
            # check calls to the directory callback
            assert [call('./pub'), ] == dir_cb.mock_calls
            # check calls to the unknown callback
            assert [] == unk_cb.mock_calls


def test_walktree_local():
    '''test the capability of walktree to walk a local directory structure'''
    wtcb = pysftp.WTCallbacks()
    pysftp.walktree('.',
                    fcallback=wtcb.file_cb,
                    dcallback=wtcb.dir_cb,
                    ucallback=wtcb.unk_cb)
    print(wtcb.dlist)
    for dname in ['./docs', './tests']:
        assert dname in wtcb.dlist

    print(wtcb.ulist)
    assert wtcb.ulist == []

    print(wtcb.flist)
    for fname in ['./release.sh', './MANIFEST.in', './tests/test_execute.py']:
        assert fname in wtcb.flist


def test_walktree_local_no_recurse():
    '''test the capability of walktree with recurse=False to walk a local
    directory structure'''
    wtcb = pysftp.WTCallbacks()
    pysftp.walktree('.',
                    fcallback=wtcb.file_cb,
                    dcallback=wtcb.dir_cb,
                    ucallback=wtcb.unk_cb,
                    recurse=False)
    print(wtcb.dlist)
    for dname in ['./docs', './tests']:
        assert dname in wtcb.dlist

    print(wtcb.ulist)
    assert wtcb.ulist == []

    print(wtcb.flist)
    for fname in ['./release.sh', './MANIFEST.in']:
        assert fname in wtcb.flist
    assert './tests/test_execute.py' not in wtcb.flist


def test_walktree_local_bad():
    '''test pysftp.walktree on a non-existing directory'''
    wtcb = pysftp.WTCallbacks()
    with pytest.raises(OSError):
        pysftp.walktree('/non-existing',
                        fcallback=wtcb.file_cb,
                        dcallback=wtcb.dir_cb,
                        ucallback=wtcb.unk_cb)
