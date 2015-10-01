'''test pysftp.Connection.get_r - uses py.test'''

import os

from tempfile import mkdtemp
import shutil

from common import VFS, conn
import pysftp


def test_get_r(sftpserver):
    '''test the get_r for remotepath is pwd '.' '''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            localpath = mkdtemp()
            sftp.get_r('.', localpath)

            checks = [([''], ['pub', 'read.me']),
                      (['', 'pub'], ['foo1', 'foo2', 'make.txt']),
                      (['', 'pub', 'foo1'], ['foo1.txt', 'image01.jpg']),
                      (['', 'pub', 'foo2'], ['bar1', 'foo2.txt']),
                      (['', 'pub', 'foo2', 'bar1'], ['bar1.txt', ]),
                      ]
            for pth, fls in checks:
                assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

            # cleanup local
            shutil.rmtree(localpath)


def test_get_r_pwd(sftpserver):
    '''test the get_r for remotepath is pwd '/pub/foo2' '''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            localpath = mkdtemp()
            sftp.get_r('pub/foo2', localpath)

            checks = [(['', ], ['pub', ]),
                      (['', 'pub', ], ['foo2', ]),
                      (['', 'pub', 'foo2'], ['bar1', 'foo2.txt']),
                      (['', 'pub', 'foo2', 'bar1'], ['bar1.txt', ]),
                      ]
            for pth, fls in checks:
                assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

            # cleanup local
            shutil.rmtree(localpath)


def test_get_r_pathed(sftpserver):
    '''test the get_r for localpath, starting deeper then pwd '''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            sftp.cwd('pub/foo2')
            localpath = mkdtemp()
            sftp.get_r('./bar1', localpath)

            checks = [(['', ], ['bar1', ]),
                      (['', 'bar1'], ['bar1.txt', ]),
                      ]
            for pth, fls in checks:
                assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

            # cleanup local
            shutil.rmtree(localpath)


def test_get_r_cdd(sftpserver):
    '''test the get_r for chdir('pub/foo2')'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            localpath = mkdtemp()
            sftp.chdir('pub/foo2')
            sftp.get_r('.', localpath)

            checks = [(['', ], ['bar1', 'foo2.txt']),
                      (['bar1', ], ['bar1.txt', ])
                      ]
            for pth, fls in checks:
                assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

            # cleanup local
            shutil.rmtree(localpath)
