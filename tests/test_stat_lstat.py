'''test pysftp.Connection.stat and .lstat - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_stat(psftp):
    '''test stat'''
    dirname = 'pub'
    psftp.chdir('/home/test')
    rslt = psftp.stat(dirname)
    assert rslt.st_size >= 0


def test_lstat(psftp):
    '''test lstat  minimal'''
    dirname = 'pub'
    psftp.chdir('/home/test')
    rslt = psftp.lstat(dirname)
    assert rslt.st_size >= 0
