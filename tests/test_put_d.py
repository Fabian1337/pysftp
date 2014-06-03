'''test pysftp.Connection.put_d - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *
from pysftp import walktree, reparent
from blddirs import build_dir_struct

from tempfile import mkdtemp
import shutil


@skip_if_ci
def test_put_d(lsftp):
    '''test put_d'''
    localpath = mkdtemp()
    print(localpath)
    remote_dir = os.path.split(localpath)[1]
    build_dir_struct(localpath)
    localpath = os.path.join(localpath, 'pub')
    print(localpath)
    # make a tidy place to put them
    lsftp.mkdir(remote_dir)
    # run the op
    lsftp.put_d(localpath, remote_dir)

    # inspect results
    rfs = pysftp.WTCallbacks()
    with lsftp.cd(remote_dir):
        lsftp.walktree('.', rfs.file_cb, rfs.dir_cb, rfs.unk_cb)

    lfs = pysftp.WTCallbacks()
    save_dir = os.getcwd()
    os.chdir(localpath)
    walktree('.', lfs.file_cb, lfs.dir_cb, lfs.unk_cb, recurse=False)
    os.chdir(save_dir)

    # cleanup remote
    for fname in rfs.flist:
        lsftp.remove(reparent(remote_dir, fname))
    for dname in reversed(rfs.dlist):
        lsftp.rmdir(reparent(remote_dir, dname))
    lsftp.rmdir(remote_dir)

    # cleanup local
    shutil.rmtree(localpath)

    # if assertions fail, give some meaningful debug out
    print("rfs", remote_dir)
    print(rfs.flist)
    print(rfs.dlist)
    print(rfs.ulist)
    print("lfs", localpath)
    print(lfs.flist)
    print(lfs.dlist)
    print(lfs.ulist)
    # check results
    assert rfs.flist == lfs.flist
    assert rfs.dlist == []
    assert rfs.ulist == lfs.ulist
    assert rfs.ulist == []

def test_put_d_ro(psftp):
    '''test put_d failure on remote read-only srvr'''
    # run the op
    with pytest.raises(IOError):
        psftp.put_d('.', '.')

def test_put_d_bad_local(psftp):
    '''test put_d failure on non-existing local directory'''
    # run the op
    with pytest.raises(OSError):
        psftp.put_d('/non-existing', '.')
