'''test pysftp module - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

from dhp.test import tempfile_containing
import pytest

# pylint: disable=E1101
# pylint: disable = W0142
SFTP_PUBLIC = {'host':'test.rebex.net', 'username':'demo',
               'password':'password'}
SFTP_LOCAL = {'host':'localhost', 'username':'test', 'password':'test1357'}
 #can only reach public, read-only server from CI platform, only test locally
 # set environment variable CI to something to disable local tests
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '')>'', reason='Not Local')

@skip_if_ci
def test_localhost():
    '''run test on localhost'''
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        assert False

def test_chdir_bad_dir():
    '''try to cwd() to a non-existing remote dir'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with pytest.raises(IOError):
            sftp.chdir('i-dont-exist')

def test_put_bad_local():
    '''try to put a non-existing file to a read-only server'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('should fail') as fname:
            pass
        # tempfile has been removed
        with pytest.raises(OSError):
            sftp.put(fname)

def test_put_not_allowed():
    '''try to put a file to a read-only server'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('should fail') as fname:
            with pytest.raises(IOError):
                sftp.put(fname)

def test_get_bad_remote():
    '''download a file'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('') as fname:
            with pytest.raises(IOError):
                sftp.get('readme-not-there.txt', fname)
            assert open(fname, 'rb').read()[0:7] != b'Welcome'

def test_connection_with():
    '''connect to a public sftp server'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.listdir() == ['pub', 'readme.txt']


def test_connection_bad_host():
    '''attempt connection to a non-existing server'''
    with pytest.raises(pysftp.ConnectionException):
        sftp = pysftp.Connection(host='',
                                 username='demo',
                                 password='password')
        sftp.close()

def test_connection_bad_credentials():
    '''attempt connection to a non-existing server'''
    with pytest.raises(pysftp.AuthenticationException):
        sftp = pysftp.Connection(host='test.rebex.net',
                                 username='demo',
                                 password='badword')
        sftp.close()

def test_connection_good():
    '''connect to a public sftp server'''
    sftp = pysftp.Connection(host='test.rebex.net',
                             username='demo',
                             password='password')
    sftp.close()


def test_listdir():
    '''try and connect to localhost'''
    sftp = pysftp.Connection(host='test.rebex.net',
                             username='demo',
                             password='password')
    assert sftp.listdir() == ['pub', 'readme.txt']
    sftp.close()


def test_cwd():
    '''try and connect to localhost'''
    sftp = pysftp.Connection(host='test.rebex.net',
                             username='demo',
                             password='password')
    assert sftp.getcwd() == None
    sftp.chdir('pub')
    assert sftp.getcwd() == '/pub'
    sftp.close()

def test_get():
    '''download a file'''
    sftp = pysftp.Connection(host='test.rebex.net',
                             username='demo',
                             password='password')
    with tempfile_containing('') as fname:
        sftp.get('readme.txt', fname)
        sftp.close()
        assert open(fname, 'rb').read()[0:7] == b'Welcome'


