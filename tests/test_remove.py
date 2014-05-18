'''test remove and unlink methods - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

from dhp.test import tempfile_containing
import pytest

# pylint: disable=E1101
# pylint: disable = W0142
SFTP_PUBLIC = {'host':'test.rebex.net', 'username':'demo',
               'password':'password'}
SFTP_LOCAL = {'host':'localhost', 'username':'test', 'password':'test1357'}
 #can only reach public, read-only server from CI platform, only test locally
 # if environment variable CI is set  to something to disable local tests
 # the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '')>'', reason='Not Local')


@skip_if_ci
def test_remove():
    '''test the remove method'''
    with tempfile_containing('*'* 8192) as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            sftp.put(fname)
            is_there = base_fname in sftp.listdir()
            sftp.remove(base_fname)
            not_there = base_fname not in sftp.listdir()

    assert is_there
    assert not_there

@skip_if_ci
def test_unlink():
    '''test the unlink function'''
    with tempfile_containing('*'* 8192) as fname:
        base_fname = os.path.split(fname)[1]
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            sftp.put(fname)
            is_there = base_fname in sftp.listdir()
            sftp.unlink(base_fname)
            not_there = base_fname not in sftp.listdir()

    assert is_there
    assert not_there

def test_remove_roserver():
    '''test reaction of attempting remove on read-only server'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with pytest.raises(IOError):
            sftp.remove('readme.txt')

@skip_if_ci
def test_remove_does_not_exist():
    '''test remove against a non-existant file'''
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        with pytest.raises(IOError):
            sftp.remove('i-am-not-here.txt')
