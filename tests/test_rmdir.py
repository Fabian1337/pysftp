'''test pysftp.Connection.rmdir - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


@skip_if_ci
def test_rmdir(lsftp):
    '''test mkdir'''
    dirname = 'test-rm'
    lsftp.mkdir(dirname)
    assert dirname in lsftp.listdir()
    lsftp.rmdir(dirname)
    assert dirname not in lsftp.listdir()


def test_rmdir_ro(psftp):
    '''test rmdir against read-only server'''
    psftp.chdir('/home/test')
    with pytest.raises(IOError):
        psftp.rmdir('pub')
