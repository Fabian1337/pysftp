'''test pysftp.Connection.get - uses py.test'''

# pylint: disable = W0142
from common import *
from mock import Mock

def test_get(psftp):
    '''download a file'''
    psftp.cwd('/home/test')
    with tempfile_containing('') as fname:
        psftp.get('/home/test/readme.txt', fname)
        assert open(fname, 'rb').read()[0:9] == b'This SFTP'

def test_get_callback(psftp):
    '''test .get callback'''
    psftp.cwd('/home/test')
    cback = Mock(return_value=None)
    with tempfile_containing('') as fname:
        result = psftp.get('readme.txt', fname, callback=cback)
        assert open(fname, 'rb').read()[0:9] == b'This SFTP'
    # verify callback was called more than once - usually a min of 2
    assert cback.call_count >= 2
    # unlike .put() nothing is returned from the operation
    assert result == None

def test_get_bad_remote(psftp):
    '''download a file'''
    psftp.cwd('/home/test')
    with tempfile_containing('') as fname:
        with pytest.raises(IOError):
            psftp.get('readme-not-there.txt', fname)
        assert open(fname, 'rb').read()[0:7] != b'Welcome'

def test_get_preserve_mtime(psftp):
    '''test that m_time is preserved from local to remote, when get'''
    psftp.cwd('/home/test')
    rfile = 'readme.txt'
    with tempfile_containing('') as localfile:
        r_stat = psftp.stat(rfile)
        psftp.get(rfile, localfile, preserve_mtime=True)
        assert r_stat.st_mtime == os.stat(localfile).st_mtime

def test_get_glob_fails(psftp):
    '''try and use get a file with a pattern - Fails'''
    psftp.cwd('/home/test')
    with tempfile_containing('') as fname:
        with pytest.raises(IOError):
            psftp.get('*', fname)
