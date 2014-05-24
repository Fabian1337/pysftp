'''test pysftp.Connection.normalize - uses py.test'''

# pylint: disable = W0142
from common import *

def test_normalize():
    '''test the normalize function'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.normalize('readme.txt') == '/home/test/readme.txt'
        assert sftp.normalize('.') == '/home/test'
        assert sftp.normalize('pub') == '/home/test/pub'
        sftp.chdir('pub')
        assert sftp.normalize('.') == '/home/test/pub'


def test_normalize_symlink():
    '''test normalize against a symlink'''
    rsym = 'readme.sym'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.normalize(rsym) == '/home/test/readme.txt'


def test_pwd():
    '''test the pwd property'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.pwd == '/home/test'
        sftp.chdir('pub')
        assert sftp.pwd == '/home/test/pub'
        sftp.chdir('src/tests')
        assert sftp.pwd == '/home/test/pub/src/tests'
