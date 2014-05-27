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
        # test they are in filename order
        assert attrs[0].filename == 'pub'
        assert attrs[1].filename == 'readme.sym'
        assert attrs[2].filename == 'readme.txt'
        # test that longname is there
        for attr in attrs:
            assert attr.longname is not None


