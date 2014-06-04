'''test pysftp module - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from mock import Mock

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
    '''try to chdir() to a non-existing remote dir'''
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

def test_connection_with():
    '''connect to a public sftp server'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.listdir() == ['pub', 'readme.sym', 'readme.txt']


def test_connection_bad_host():
    '''attempt connection to a non-existing server'''
    with pytest.raises(pysftp.ConnectionException):
        sftp = pysftp.Connection(host='',
                                 username='demo',
                                 password='password')
        sftp.close()

def test_connection_bad_credentials():
    '''attempt connection to a non-existing server'''
    with pytest.raises(pysftp.SSHException):
        copts = SFTP_PUBLIC.copy()
        copts['password'] = 'badword'
        with pysftp.Connection(**copts) as sftp:
            pass

def test_connection_good():
    '''connect to a public sftp server'''
    sftp = pysftp.Connection(**SFTP_PUBLIC)
    sftp.close()


def test_getcwd():
    '''test .getcwd'''
    sftp = pysftp.Connection(**SFTP_PUBLIC)
    assert sftp.getcwd() == None
    sftp.chdir('pub')
    assert sftp.getcwd() == '/home/test/pub'
    sftp.close()


