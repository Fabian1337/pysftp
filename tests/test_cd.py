'''test pysftp.Connection.cd - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *


def test_cd_none():
    '''test .cd with None'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        home = sftp.pwd
        with sftp.cd():
            sftp.chdir('pub')
            assert sftp.pwd == '/home/test/pub'
        assert home == sftp.pwd

def test_cd_path():
    '''test .cd with a path'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        home = sftp.pwd
        with sftp.cd('pub'):
            assert sftp.pwd == '/home/test/pub'
        assert home == sftp.pwd

def test_cd_nested():
    '''test nested cd's'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        home = sftp.pwd
        with sftp.cd('pub'):
            assert sftp.pwd == '/home/test/pub'
            with sftp.cd('example'):
                assert sftp.pwd == '/home/test/pub/example'
            assert sftp.pwd == '/home/test/pub'
        assert home == sftp.pwd

def test_cd_bad_path():
    '''test .cd with a bad path'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
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
    '''test pysftp.cd on non-existing directory'''
    with pytest.raises(OSError):
        with pysftp.cd('not-there'):
            pass
