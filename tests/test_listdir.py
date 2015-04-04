'''test pysftp.Connection.listdir - uses py.test'''

# pylint: disable = W0142
from common import *


def test_listdir(sftpserver):
    '''test listdir'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub')
            assert psftp.listdir() == ['foo1', 'foo2', 'make.txt']


def test_listdir_attr(sftpserver):
    '''test listdir'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            psftp.cwd('/pub')
            attrs = psftp.listdir_attr()
            assert len(attrs) == 3
            # test they are in filename order
            assert attrs[0].filename == 'foo1'
            assert attrs[1].filename == 'foo2'
            assert attrs[2].filename == 'make.txt'
            # test that longname is there
            for attr in attrs:
                assert attr.longname is not None
