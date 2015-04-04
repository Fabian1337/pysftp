'''test pysftp.Connection.cd - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *


def test_cd_none(sftpserver):
    '''test .cd with None'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            home = psftp.pwd
            with psftp.cd():
                psftp.chdir('pub')
                assert psftp.pwd == '/pub'
            assert home == psftp.pwd


def test_cd_path(sftpserver):
    '''test .cd with a path'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            home = psftp.pwd
            with psftp.cd('pub'):
                assert psftp.pwd == '/pub'
            assert home == psftp.pwd


def test_cd_nested(sftpserver):
    '''test nested cd's'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            home = psftp.pwd
            with psftp.cd('pub'):
                assert psftp.pwd == '/pub'
                with psftp.cd('foo1'):
                    assert psftp.pwd == '/pub/foo1'
                assert psftp.pwd == '/pub'
            assert home == psftp.pwd


def test_cd_bad_path(sftpserver):
    '''test .cd with a bad path'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            home = psftp.pwd
            with pytest.raises(IOError):
                with psftp.cd('not-there'):
                    pass
            assert home == psftp.pwd


def test_cd_local():
    '''test pysftp.cd on local directories'''
    original = os.getcwd()
    with pysftp.cd('docs'):
        assert os.getcwd() == os.path.join(original, 'docs')
    assert os.getcwd() == original


def test_cd_local_bad():
    '''test pysftp.cd on non-existing directory'''
    with pytest.raises(OSError):
        with pysftp.cd('not-there'):
            pass
