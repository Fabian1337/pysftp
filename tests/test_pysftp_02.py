'''test pysftp module - set 2 - uses py.test'''
# psftp and lsftp fixtures are from conftest.py
# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from stat import S_ISLNK


def test_sftp_client(psftp):
    '''test for access to the underlying, active sftpclient'''
    # with pysftp.Connection(**SFTP_PUBLIC) as sftp:
    #     assert 'normalize' in dir(sftp.sftp_client)
    #     assert 'readlink' in dir(sftp.sftp_client)
    assert 'normalize' in dir(psftp.sftp_client)
    assert 'readlink' in dir(psftp.sftp_client)


def test_path_retreat():
    '''test path_retreat generator'''
    pth = 'foo/bar/baz'
    assert list(pysftp.path_retreat(pth)) == ['foo/bar/baz',
                                              'foo/bar',
                                              'foo']
    pth = '/foo/bar/baz'
    assert list(pysftp.path_retreat(pth)) == ['/foo/bar/baz',
                                              '/foo/bar',
                                              '/foo']


def test_path_advance():
    '''test path_advance generator'''
    pth = 'foo/bar/baz'
    assert list(pysftp.path_advance(pth)) == ['foo',
                                              'foo/bar',
                                              'foo/bar/baz']
    pth = '/foo/bar/baz'
    assert list(pysftp.path_advance(pth)) == ['/foo',
                                              '/foo/bar',
                                              '/foo/bar/baz']


@skip_if_ci
def test_makedirs(lsftp):
    '''test makedirs simple, testing 2 things, oh well'''
    rdir = 'foo/bar/baz'
    rdir2 = 'foo/bar'
    assert lsftp.exists(rdir) is False
    lsftp.makedirs(rdir)
    is_dir = lsftp.isdir(rdir)
    lsftp.rmdir(rdir)
    lsftp.rmdir(rdir2)
    lsftp.makedirs(rdir)     # try partially existing path
    is_dir_partial = lsftp.isdir(rdir)
    for rpath in pysftp.path_retreat(rdir):
        lsftp.rmdir(rpath)
    assert is_dir
    assert is_dir_partial


def test_lexists_symbolic(psftp):
    '''test .lexists() vs. symbolic link'''
    rsym = 'readme.sym'
    assert psftp.lexists(rsym)


@skip_if_ci
def test_symlink(lsftp):
    '''test symlink creation'''
    rdest = '/home/test/honey-boo-boo'
    with tempfile_containing(contents=8192*'*') as fname:
        lsftp.put(fname)
        lsftp.symlink(fname, rdest)
        rslt = lsftp.lstat(rdest)
        is_link = S_ISLNK(rslt.st_mode)
        lsftp.remove(rdest)
        lsftp.remove(os.path.split(fname)[1])
    assert is_link


def test_exists(psftp):
    '''test .exists() fuctionality'''
    rfile = '/home/test/readme.txt'
    rbad = '/home/test/peek-a-boo.txt'
    assert psftp.exists(rfile)
    assert psftp.exists(rbad) is False
    assert psftp.exists('pub')


def test_lexists(psftp):
    '''test .lexists() functionality'''
    rfile = '/home/test/readme.txt'
    rbad = '/home/test/peek-a-boo.txt'
    assert psftp.lexists(rfile)
    assert psftp.lexists(rbad) is False
    assert psftp.lexists('pub')
