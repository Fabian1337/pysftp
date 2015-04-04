'''test pysftp.Connection.get - uses py.test'''

# pylint: disable = W0142
from common import *
from mock import Mock


def test_get(sftpserver):
    '''download a file'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub/foo1')
            with tempfile_containing('') as fname:
                psftp.get('/pub/foo1/foo1.txt', fname)
                assert open(fname, 'rb').read() == b'content of foo1.txt'


def test_get_callback(sftpserver):
    '''test .get callback'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub/foo1')
            cback = Mock(return_value=None)
            with tempfile_containing('') as fname:
                result = psftp.get('foo1.txt', fname, callback=cback)
                assert open(fname, 'rb').read() == b'content of foo1.txt'
            # verify callback was called more than once - usually a min of 2
            assert cback.call_count >= 2
            # unlike .put() nothing is returned from the operation
            assert result is None


def test_get_bad_remote(sftpserver):
    '''download a file'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub/foo1')
            with tempfile_containing('') as fname:
                with pytest.raises(IOError):
                    psftp.get('readme-not-there.txt', fname)
                assert open(fname, 'rb').read()[0:7] != b'Welcome'


def test_get_preserve_mtime(sftpserver):
    '''test that m_time is preserved from local to remote, when get'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub/foo1')
            rfile = 'foo1.txt'
            with tempfile_containing('') as localfile:
                r_stat = psftp.stat(rfile)
                psftp.get(rfile, localfile, preserve_mtime=True)
                assert r_stat.st_mtime == os.stat(localfile).st_mtime


def test_get_glob_fails(sftpserver):
    '''try and use get a file with a pattern - Fails'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub/foo1')
            with tempfile_containing('') as fname:
                with pytest.raises(IOError):
                    psftp.get('*', fname)
