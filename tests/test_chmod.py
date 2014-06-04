'''test pysftp.Connection.chmod - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
import pytest

def test_chmod_not_exist(psftp):
    '''verify error if trying to chmod something that isn't there'''
    with pytest.raises(IOError):
        psftp.chmod('i-do-not-exist.txt', 666)

@skip_if_ci
def test_chmod_simple(lsftp):
    '''test basic chmod with octal mode represented by an int`'''
    new_mode = 744      #user=rwx g=r o=r
    with tempfile_containing('') as fname:
        base_fname = os.path.split(fname)[1]
        org_attrs = lsftp.put(fname)
        lsftp.chmod(base_fname, new_mode)
        new_attrs = lsftp.stat(base_fname)
        lsftp.remove(base_fname)
    # that the new mod 711 is as we wanted
    assert pysftp.st_mode_to_int(new_attrs.st_mode) == new_mode
    # that we actually changed something
    assert new_attrs.st_mode != org_attrs.st_mode

def test_chmod_fail_ro(psftp):
    '''test chmod against read-only server'''
    new_mode = 440
    fname = 'readme.txt'
    with pytest.raises(IOError):
        psftp.chmod(fname, new_mode)      #make sure we start from a known mode

