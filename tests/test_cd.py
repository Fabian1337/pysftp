'''test pysftp.Connection.cd - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *


def test_cd_none(psftp):
    '''test .cd with None'''
    home = psftp.pwd
    with psftp.cd():
        psftp.chdir('pub')
        assert psftp.pwd == '/home/test/pub'
    assert home == psftp.pwd

def test_cd_path(psftp):
    '''test .cd with a path'''
    home = psftp.pwd
    with psftp.cd('pub'):
        assert psftp.pwd == '/home/test/pub'
    assert home == psftp.pwd

def test_cd_nested(psftp):
    '''test nested cd's'''
    home = psftp.pwd
    with psftp.cd('pub'):
        assert psftp.pwd == '/home/test/pub'
        with psftp.cd('example'):
            assert psftp.pwd == '/home/test/pub/example'
        assert psftp.pwd == '/home/test/pub'
    assert home == psftp.pwd

def test_cd_bad_path(psftp):
    '''test .cd with a bad path'''
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
