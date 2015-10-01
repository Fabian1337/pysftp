'''test pysftp.Connection.cd - uses py.test'''
from __future__ import print_function
import os

import pytest

from common import VFS, conn
import pysftp


def test_cd_none(sftpserver):
    '''test .cd with None'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            home = sftp.pwd
            with sftp.cd():
                sftp.chdir('pub')
                assert sftp.pwd == '/home/test/pub'
            assert home == sftp.pwd


def test_cd_path(sftpserver):
    '''test .cd with a path'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            home = sftp.pwd
            with sftp.cd('pub'):
                assert sftp.pwd == '/home/test/pub'
            assert home == sftp.pwd


def test_cd_nested(sftpserver):
    '''test nested cd's'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            home = sftp.pwd
            with sftp.cd('pub'):
                assert sftp.pwd == '/home/test/pub'
                with sftp.cd('foo1'):
                    assert sftp.pwd == '/home/test/pub/foo1'
                assert sftp.pwd == '/home/test/pub'
            assert home == sftp.pwd


def test_cd_bad_path(sftpserver):
    '''test .cd with a bad path'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            home = sftp.pwd
            with pytest.raises(IOError):
                with sftp.cd('not-there'):
                    pass
            assert home == sftp.pwd


def test_cd_local():
    '''test pysftp.cd on local directories'''
    original = os.getcwd()
    with pysftp.cd('docs'):
        assert os.getcwd() == os.path.join(original, 'docs')
    assert os.getcwd() == original


def test_cd_local_bad():
    '''test pysftp.cd on non-existing local directory'''
    with pytest.raises(OSError):
        with pysftp.cd('not-there'):
            pass
