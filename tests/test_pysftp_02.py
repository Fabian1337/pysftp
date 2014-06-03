'''test pysftp module - set 2 - uses py.test'''
# psftp and lsftp fixtures are from conftest.py
# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from stat import S_ISLNK
from time import sleep


def test_sftp_client(psftp):
    '''test for access to the underlying, active sftpclient'''
    # with pysftp.Connection(**SFTP_PUBLIC) as sftp:
    #     assert 'normalize' in dir(sftp.sftp_client)
    #     assert 'readlink' in dir(sftp.sftp_client)
    assert 'normalize' in dir(psftp.sftp_client)
    assert 'readlink' in dir(psftp.sftp_client)

@skip_if_ci
def test_chown_uid(lsftp):
    '''test changing just the uid'''
    # with tempfile_containing('contents') as fname:
    #     base_fname = base_fname = os.path.split(fname)[1]
    #     with pysftp.Connection(**SFTP_LOCAL) as sftp:
    #         org_attrs = sftp.put(fname)
    #         uid = org_attrs.st_uid  # - 1
    #         sftp.chown(base_fname, uid=uid)
    #         new_attrs = sftp.stat(base_fname)
    #         sftp.remove(base_fname)
    # assert new_attrs.st_uid == uid
    # assert new_attrs.st_gid == org_attrs.st_gid  # confirm no change to gid
    with tempfile_containing('contents') as fname:
        base_fname = base_fname = os.path.split(fname)[1]
        org_attrs = lsftp.put(fname)
        uid = org_attrs.st_uid  # - 1
        lsftp.chown(base_fname, uid=uid)
        new_attrs = lsftp.stat(base_fname)
        lsftp.remove(base_fname)
    assert new_attrs.st_uid == uid
    assert new_attrs.st_gid == org_attrs.st_gid  # confirm no change to gid

@skip_if_ci
def test_chown_gid(lsftp):
    '''test changing just the gid'''
    # with tempfile_containing('contents') as fname:
    #     base_fname = base_fname = os.path.split(fname)[1]
    #     with pysftp.Connection(**SFTP_LOCAL) as sftp:
    #         org_attrs = sftp.put(fname)
    #         gid = org_attrs.st_gid  # - 1
    #         sftp.chown(base_fname, gid=gid)
    #         new_attrs = sftp.stat(base_fname)
    #         sftp.remove(base_fname)
    # assert new_attrs.st_gid == gid
    # assert new_attrs.st_uid == org_attrs.st_uid  # confirm no change to uid
    with tempfile_containing('contents') as fname:
        base_fname = base_fname = os.path.split(fname)[1]
        org_attrs = lsftp.put(fname)
        gid = org_attrs.st_gid  # - 1
        lsftp.chown(base_fname, gid=gid)
        new_attrs = lsftp.stat(base_fname)
        lsftp.remove(base_fname)
    assert new_attrs.st_gid == gid
    assert new_attrs.st_uid == org_attrs.st_uid  # confirm no change to uid

@skip_if_ci
def test_chown_none():
    '''call .chown with no gid or uid specified'''
    with tempfile_containing('contents') as fname:
        base_fname = base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            org_attrs = sftp.put(fname)
            sftp.chown(base_fname)
            new_attrs = sftp.stat(base_fname)
            sftp.remove(base_fname)
    assert new_attrs.st_gid == org_attrs.st_gid
    assert new_attrs.st_uid == org_attrs.st_uid  # confirm no change to uid

@skip_if_ci
def test_chown_not_exist():
    '''call .chown on a non-existing path'''
    with pytest.raises(IOError):
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            sftp.chown('i-do-not-exist.txt', 666)

def test_chown_ro_server():
    '''call .chown against path on read-only server'''
    with pytest.raises(IOError):
        with pysftp.Connection(**SFTP_PUBLIC) as sftp:
            sftp.chown('readme.txt', gid=1000, uid=1000)

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
def test_makedirs():
    '''test makedirs simple, testing 2 things, oh well'''
    rdir = 'foo/bar/baz'
    rdir2 = 'foo/bar'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        assert sftp.exists(rdir) == False
        sftp.makedirs(rdir)
        is_dir = sftp.isdir(rdir)
        sftp.rmdir(rdir)
        sftp.rmdir(rdir2)
        sftp.makedirs(rdir)     # try partially existing path
        is_dir_partial = sftp.isdir(rdir)
        for rpath in pysftp.path_retreat(rdir):
            sftp.rmdir(rpath)
    assert is_dir
    assert is_dir_partial

def test_isfile():
    '''test .isfile() functionality'''
    rfile = 'readme.txt'
    rdir = 'pub'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.isfile(rfile) == True
        assert sftp.isfile(rdir) == False

def test_isfile_2():
    '''test .isfile() functionality against a symlink'''
    rsym = 'readme.sym'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.isfile(rsym)

def test_isdir():
    '''test .isdir() functionality'''
    rfile = 'readme.txt'
    rdir = 'pub'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.isdir(rfile) == False
        assert sftp.isdir(rdir) == True

def test_isdir_2():
    '''test .isdir() functionality against a symlink'''
    rsym = 'readme.sym'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.isdir(rsym) == False

def test_lexists_symbolic():
    '''test .lexists() vs. symbolic link'''
    rsym = 'readme.sym'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.lexists(rsym)

@skip_if_ci
def test_symlink():
    '''test symlink creation'''
    rdest = 'honey-boo-boo'
    with tempfile_containing(contents=8192*'*') as fname:
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            sftp.put(fname)
            sftp.symlink(fname, rdest)
            rslt = sftp.lstat(rdest)
            is_link = S_ISLNK(rslt.st_mode) == True
            sftp.remove(rdest)
            sftp.remove(os.path.split(fname)[1])
    assert is_link

def test_exists():
    '''test .exists() fuctionality'''
    rfile = 'readme.txt'
    rbad = 'pee-a-boo.txt'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.exists(rfile) == True
        assert sftp.exists(rbad) == False
        assert sftp.exists('pub') == True

def test_lexists():
    '''test .lexists() functionality'''
    rfile = 'readme.txt'
    rbad = 'pee-a-boo.txt'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.lexists(rfile) == True
        assert sftp.lexists(rbad) == False
        assert sftp.lexists('pub') == True

def test_get_preserve_mtime():
    '''test that m_time is preserved from local to remote, when get'''
    rfile = 'readme.txt'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('') as localfile:
            r_stat = sftp.stat(rfile)
            sftp.get(rfile, localfile, preserve_mtime=True)
            assert r_stat.st_mtime == os.stat(localfile).st_mtime

@skip_if_ci
def test_put_preserve_mtime(lsftp):
    '''test that m_time is preserved from local to remote, when put'''
    with tempfile_containing(contents=8192*'*') as fname:
        base_fname = os.path.split(fname)[1]
        base = os.stat(fname)
        # with pysftp.Connection(**SFTP_LOCAL) as sftp:
        result1 = lsftp.put(fname, preserve_mtime=True)
        sleep(2)
        result2 = lsftp.put(fname, preserve_mtime=True)
        # clean up
        lsftp.remove(base_fname)
    # see if times are modified
    # assert base.st_atime == result1.st_atime
    assert base.st_mtime == result1.st_mtime
    # assert result1.st_atime == result2.st_atime
    assert result1.st_mtime == result2.st_mtime

