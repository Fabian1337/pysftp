'''test pysftp.Connection.get_d - uses py.test'''

import os

from tempfile import mkdtemp
import shutil

from common import VFS, conn
import pysftp


def test_get_d(sftpserver):
    '''test the get_d for remotepath is pwd '.' '''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            sftp.cwd('pub')
            localpath = mkdtemp()
            sftp.get_d('.', localpath)

            checks = [(['', ], ['make.txt', ]), ]
            for pth, fls in checks:
                assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

            # cleanup local
            shutil.rmtree(localpath)


def test_get_d_pathed(sftpserver):
    '''test the get_d for localpath, starting deeper then pwd '''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            sftp.cwd('pub')
            localpath = mkdtemp()
            sftp.get_d('foo1', localpath)

            chex = [(['', ],
                     ['foo1.txt', 'image01.jpg']), ]
            for pth, fls in chex:
                assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

            # cleanup local
            shutil.rmtree(localpath)
