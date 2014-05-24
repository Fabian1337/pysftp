'''test pysftp.Connection.listdir - uses py.test'''

# pylint: disable = W0142
from common import *

def test_listdir():
    '''test listdir'''
    sftp = pysftp.Connection(**SFTP_PUBLIC)
    assert sftp.listdir() == ['pub', 'readme.sym', 'readme.txt']
    sftp.close()


def test_listdir_attr():
    '''test listdir'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        attrs = sftp.listdir_attr()
        assert len(attrs) == 3
        for attr in attrs:
            assert attr.filename in ['pub', 'readme.sym', 'readme.txt']
            assert attr.longname is not None


