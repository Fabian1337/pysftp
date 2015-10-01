'''test remove and unlink methods - uses py.test'''

import os

from dhp.test import tempfile_containing
import pytest

from common import skip_if_ci


@skip_if_ci
def test_remove(lsftp):
    '''test the remove method'''
    with tempfile_containing('*' * 8192) as fname:
        base_fname = os.path.split(fname)[1]
        lsftp.chdir('/home/test')
        lsftp.put(fname)
        is_there = base_fname in lsftp.listdir()
        lsftp.remove(base_fname)
        not_there = base_fname not in lsftp.listdir()

    assert is_there
    assert not_there


@skip_if_ci
def test_unlink(lsftp):
    '''test the unlink function'''
    with tempfile_containing('*' * 8192) as fname:
        base_fname = os.path.split(fname)[1]
        lsftp.chdir('/home/test')
        lsftp.put(fname)
        is_there = base_fname in lsftp.listdir()
        lsftp.unlink(base_fname)
        not_there = base_fname not in lsftp.listdir()

    assert is_there
    assert not_there


# TODO
# def test_remove_roserver(psftp):
#     '''test reaction of attempting remove on read-only server'''
#     psftp.chdir('/home/test')
#     with pytest.raises(IOError):
#         psftp.remove('readme.txt')


@skip_if_ci
def test_remove_does_not_exist(lsftp):
    '''test remove against a non-existant file'''
    lsftp.chdir('/home/test')
    with pytest.raises(IOError):
        lsftp.remove('i-am-not-here.txt')
