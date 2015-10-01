'''test issues raised here if they don't fit else where - uses py.test'''
from __future__ import print_function

import os
from tempfile import mkdtemp
import shutil

from common import skip_if_ci, VFS, conn
from blddirs import build_dir_struct
from pysftp import reparent
import pysftp


@skip_if_ci
def test_issue_15(lsftp):
    '''chdir followed by execute doesn't occur in expected directory.'''
    hresults = lsftp.execute('pwd')
    lsftp.chdir('/home/test')
    assert hresults == lsftp.execute('pwd')
    # .exec operates independently of the current working directory .pwd


def test_issue_67(sftpserver):
    """isdir fails if you don't specify a root path"""
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            assert sftp.isdir('pub')


@skip_if_ci
def test_issue_63(lsftp):
    '''put_r-fails-when-overwriting-directory'''
    localpath = mkdtemp()
    print(localpath)
    remote_dir = os.path.split(localpath)[1]
    build_dir_struct(localpath)
    localpath = os.path.join(localpath, 'pub')
    print(localpath)
    # make a tidy place to put them
    lsftp.mkdir(remote_dir)
    # run the op
    lsftp.put_r(localpath, remote_dir)
    try:
        lsftp.put_r(localpath, remote_dir)
        failed = False
    except IOError:
        failed = True

    # inspect results
    rfs = pysftp.WTCallbacks()
    with lsftp.cd(remote_dir):
        lsftp.walktree('.', rfs.file_cb, rfs.dir_cb, rfs.unk_cb)

    # cleanup remote
    for fname in rfs.flist:
        lsftp.remove(reparent(remote_dir, fname))
    for dname in reversed(rfs.dlist):
        lsftp.rmdir(reparent(remote_dir, dname))
    lsftp.rmdir(remote_dir)

    # cleanup local
    shutil.rmtree(os.path.split(localpath)[0])

    # assert that it worked without throwing an error
    assert not failed
