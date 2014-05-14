'''test pysftp module - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

from io import BytesIO

import pysftp

from dhp.test import tempfile_containing
from mock import Mock, call
import pytest

# pylint: disable=E1101
# pylint: disable = W0142
SFTP_PUBLIC = {'host':'test.rebex.net', 'username':'demo',
               'password':'password'}
SFTP_LOCAL = {'host':'localhost', 'username':'test', 'password':'test1357'}
 #can only reach public, read-only server from CI platform, only test locally
 # if environment variable CI is set  to something to disable local tests
 # the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '')>'', reason='Not Local')



@skip_if_ci
def test_putfo_callback_fsize():
    '''test putfo with callback and file_size'''
    rfile = 'a-test-file'
    buf = 'I will not buy this record, it is scratched\nMy hovercraft'\
    ' is full of eels.'
    fsize = len(buf)
    bwrote = fsize
    flo = BytesIO(buf)
    cback = Mock(return_value=None)
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        sftp.putfo(flo, rfile, file_size=fsize, callback=cback)
        sftp.remove(rfile)
    assert cback.call_count >= 2
    # we didn't specify file size, so second arg is 0
    assert cback.call_args_list == [call(bwrote, fsize), call(bwrote, fsize)]

@skip_if_ci
def test_putfo_callback():
    '''test putfo with callback'''
    rfile = 'a-test-file'
    buf = 'I will not buy this record, it is scratched\nMy hovercraft'\
    ' is full of eels.'
    flo = BytesIO(buf)
    cback = Mock(return_value=None)
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        sftp.putfo(flo, rfile, callback=cback)
        sftp.remove(rfile)
    assert cback.call_count >= 2
    # we didn't specify file size, so second arg is 0
    assert cback.call_args_list == [call(len(buf), 0), call(len(buf), 0)]

@skip_if_ci
def test_putfo_flo():
    '''test putfo in simple form'''
    rfile = 'a-test-file'
    buf = 'I will not buy this record, it is scratched\nMy hovercraft'\
    ' is full of eels.'
    flo = BytesIO(buf)
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        assert rfile not in sftp.listdir()
        rslt = sftp.putfo(flo, rfile)
        assert rfile in sftp.listdir()
        sftp.remove(rfile)
    assert rslt.st_size == len(buf)

@skip_if_ci
def test_putfo_no_remotepath():
    '''test putfo raises TypeError when not specifying a remotepath'''
    buf = 'I will not buy this record, it is scratched\nMy hovercraft'\
    ' is full of eels.'
    flo = BytesIO(buf)
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        with pytest.raises(TypeError):
            sftp.putfo(flo)

def test_getfo_flo():
    '''test getfo to a file-like object'''
    flo = BytesIO()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        num_bytes = sftp.getfo('readme.txt', flo)

    assert flo.getvalue()[0:7] == b'Welcome'
    assert num_bytes == len(flo.getvalue())

def test_getfo_callback():
    '''test getfo callback'''
    flo = BytesIO()
    cback = Mock(return_value=None)
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.getfo('readme.txt', flo, callback=cback)

    assert cback.call_count >= 2

@skip_if_ci
def test_mkdir_mode():
    '''test mkdir with mode set to 711'''
    dirname = 'test-dir'
    mode = 711
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        assert dirname not in sftp.listdir()
        sftp.mkdir(dirname, mode=mode)
        attrs = sftp.stat(dirname)
        sftp.rmdir(dirname)
        assert pysftp.st_mode_to_int(attrs.st_mode) == mode

@skip_if_ci
def test_mkdir():
    '''test mkdir'''
    dirname = 'test-dir'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        assert dirname not in sftp.listdir()
        sftp.mkdir(dirname)
        assert dirname in sftp.listdir()
        # clean up
        sftp.rmdir(dirname)

@skip_if_ci
def test_rmdir():
    '''test mkdir'''
    dirname = 'test-rm'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        sftp.mkdir(dirname)
        assert dirname in sftp.listdir()
        sftp.rmdir(dirname)
        assert dirname not in sftp.listdir()

def test_stat():
    '''test stat'''
    dirname = 'pub'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        rslt = sftp.stat(dirname)
    assert rslt.st_size >= 0

def test_lstat():
    '''test lstat  minimal'''
    dirname = 'pub'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        rslt = sftp.lstat(dirname)
    assert rslt.st_size >= 0

def test_issue_15():
    '''chdir followed by execute doesn't occur in expected directory.'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        hresults = sftp.execute('pwd')
        sftp.chdir('pub')
        assert hresults == sftp.execute('pwd')

def test_open_read():
    '''test the open function'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        rfile = sftp.open('readme.txt')
        contents = rfile.read()
        rfile.close()
    assert contents[0:7] == b'Welcome'

@skip_if_ci
def test_put_callback_confirm():
    '''test the callback and confirm feature of put'''
    cback = Mock(return_value=None)
    with tempfile_containing(contents=8192*'*') as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            result = sftp.put(fname, callback=cback)
            # clean up
            sftp.remove(base_fname)
    # verify callback was called more than once - usually a min of 2
    assert cback.call_count >= 2
    # verify that an SFTPAttribute like os.stat was returned
    assert result.st_size == 8192
    assert result.st_uid
    assert result.st_gid
    assert result.st_atime
    assert result.st_mtime

@skip_if_ci
def test_rename():
    '''test rename on remote'''
    contents = 'now is the time\nfor all good...'
    with tempfile_containing(contents=contents) as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            if base_fname in sftp.listdir():
                sftp.remove(base_fname)
            assert base_fname not in sftp.listdir()
            sftp.put(fname)
            sftp.rename(base_fname, 'bob')
            rdirs = sftp.listdir()
            assert 'bob' in rdirs
            assert base_fname not in rdirs
            sftp.remove('bob')

@skip_if_ci
def test_put():
    '''run test on localhost'''
    contents = 'now is the time\nfor all good...'
    with tempfile_containing(contents=contents) as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            if base_fname in sftp.listdir():
                sftp.remove(base_fname)
            assert base_fname not in sftp.listdir()
            sftp.put(fname)
            assert base_fname in sftp.listdir()
            with tempfile_containing('') as tfile:
                sftp.get(base_fname, tfile)
                assert open(tfile).read() == contents
            # clean up
            sftp.remove(base_fname)


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

def test_get_callback():
    '''download a file'''
    cback = Mock(return_value=None)
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('') as fname:
            result = sftp.get('readme.txt', fname, callback=cback)
            assert open(fname, 'rb').read()[0:7] == b'Welcome'
    # verify callback was called more than once - usually a min of 2
    assert cback.call_count >= 2
    # unlike .put() nothing is returned from the operation
    assert result == None

