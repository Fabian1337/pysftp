'''test pysftp.Connection.mkdir - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


@skip_if_ci
def test_mkdir_mode(lsftp):
    '''test mkdir with mode set to 711'''
    dirname = 'test-dir'
    mode = 711
    assert dirname not in lsftp.listdir()
    lsftp.mkdir(dirname, mode=mode)
    attrs = lsftp.stat(dirname)
    lsftp.rmdir(dirname)
    assert pysftp.st_mode_to_int(attrs.st_mode) == mode


@skip_if_ci
def test_mkdir(lsftp):
    '''test mkdir'''
    dirname = 'test-dir'
    assert dirname not in lsftp.listdir()
    lsftp.mkdir(dirname)
    assert dirname in lsftp.listdir()
    # clean up
    lsftp.rmdir(dirname)


def test_mkdir_ro(psftp):
    '''test mkdir on a read-only server'''
    dirname = 'test-dir'
    assert dirname not in psftp.listdir()
    with pytest.raises(IOError):
        psftp.mkdir(dirname)
