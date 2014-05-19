'''test pysftp.Connection.normalize - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

from io import BytesIO
import pytest
import pysftp

# pylint: disable=E1101
# pylint: disable = W0142
SFTP_PUBLIC = {'host':'test.rebex.net', 'username':'demo',
               'password':'password'}
SFTP_LOCAL = {'host':'localhost', 'username':'test', 'password':'test1357'}
 #can only reach public, read-only server from CI platform, only test locally
 # if environment variable CI is set  to something to disable local tests
 # the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '')>'', reason='Not Local')

def test_normalize():
    '''test the normalize function'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.normalize('readme.txt') == '/readme.txt'
        assert sftp.normalize('.') == '/'
        assert sftp.normalize('pub') == '/pub'
        sftp.chdir('pub')
        assert sftp.normalize('.') == '/pub'

@skip_if_ci
def test_normalize_symlink():
    '''test normalize against a symlink'''
    flo = BytesIO('*'*8192)
    rfile = 'read-me.txt'
    rsym = 'read-me.sym'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        sftp.putfo(flo, rfile)
        sftp.symlink(rfile, rsym)
        rslvs_correct = sftp.normalize(rsym) == '/home/test/read-me.txt'
        # clean up
        sftp.remove(rfile)
        sftp.remove(rsym)
    assert rslvs_correct
