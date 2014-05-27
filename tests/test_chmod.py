'''test pysftp.Connection.chmod - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *
import pytest

def test_chmod_not_exist():
    '''verify error if trying to chmod something that isn't there'''
    with pytest.raises(IOError):
        with pysftp.Connection(**SFTP_PUBLIC) as sftp:
            sftp.chmod('i-do-not-exist.txt', 666)

@skip_if_ci
def test_chmod_simple():
    '''test basic chmod with octal mode represented by an int`'''
    new_mode = 744      #user=rwx g=r o=r
    with tempfile_containing('') as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            org_attrs = sftp.put(fname)
            sftp.chmod(base_fname, new_mode)
            new_attrs = sftp.stat(base_fname)
            sftp.remove(base_fname)
    # that the new mod 711 is as we wanted
    assert pysftp.st_mode_to_int(new_attrs.st_mode) == new_mode
    # that we actually changed something
    assert new_attrs.st_mode != org_attrs.st_mode

def test_chmod_fail_ro():
    '''test chmod against read-only server'''
    new_mode = 440
    fname = 'readme.txt'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.chmod(fname, 444)      #make sure we start from a known mode
        org_attrs = sftp.stat(fname)
        sftp.chmod(fname, new_mode)
        new_attrs = sftp.stat(fname)
        #reset the mode back
        sftp.chmod(fname, pysftp.st_mode_to_int(org_attrs.st_mode))

    # that the new mod 740 is as we wanted
    assert pysftp.st_mode_to_int(new_attrs.st_mode) == new_mode
    # that we actually changed something
    assert new_attrs.st_mode != org_attrs.st_mode
    assert pysftp.st_mode_to_int(org_attrs.st_mode) == 444

