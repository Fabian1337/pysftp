'''test pysftp.Connection.normalize - uses py.test'''

# pylint: disable = W0142
from common import *

def test_normalize(psftp):
    '''test the normalize function'''
    psftp.chdir('/home/test')
    assert psftp.normalize('readme.txt') == '/home/test/readme.txt'
    assert psftp.normalize('.') == '/home/test'
    assert psftp.normalize('pub') == '/home/test/pub'
    psftp.chdir('pub')
    assert psftp.normalize('.') == '/home/test/pub'


def test_normalize_symlink(psftp):
    '''test normalize against a symlink'''
    psftp.chdir('/home/test')
    rsym = 'readme.sym'
    assert psftp.normalize(rsym) == '/home/test/readme.txt'


def test_pwd(psftp):
    '''test the pwd property'''
    psftp.chdir('/home/test')
    assert psftp.pwd == '/home/test'
    psftp.chdir('pub')
    assert psftp.pwd == '/home/test/pub'
    psftp.chdir('src/tests')
    assert psftp.pwd == '/home/test/pub/src/tests'
