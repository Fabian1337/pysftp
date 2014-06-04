'''test pysftp.Connection.isX methods - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *

def test_isfile(psftp):
    '''test .isfile() functionality'''
    rfile = '/home/test/readme.txt'
    rdir = 'pub'
    assert psftp.isfile(rfile) == True
    assert psftp.isfile(rdir) == False

def test_isfile_2(psftp):
    '''test .isfile() functionality against a symlink'''
    rsym = '/home/test/readme.sym'
    assert psftp.isfile(rsym)

def test_isdir(psftp):
    '''test .isdir() functionality'''
    rfile = '/home/test/readme.txt'
    rdir = '/home/test/pub'
    assert psftp.isdir(rfile) == False
    assert psftp.isdir(rdir) == True

def test_isdir_2(psftp):
    '''test .isdir() functionality against a symlink'''
    rsym = '/home/test/readme.sym'
    assert psftp.isdir(rsym) == False

