'''test pysftp.Connection.listdir - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

from io import BytesIO
import pysftp

import pytest

# pylint: disable=E1101
# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}
SFTP_LOCAL = {'host':'localhost', 'username':'test', 'password':'test1357'}
 #can only reach public, read-only server from CI platform, only test locally
 # if environment variable CI is set  to something to disable local tests
 # the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '')>'', reason='Not Local')


@skip_if_ci
def test_truncate_smaller():
    '''test truncate, make file smaller'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        try:
            sftp.remove(rname)
        except IOError:
            pass
        sftp.putfo(flo, rname)
        new_size = sftp.truncate(rname, 4096)
        assert new_size == 4096
        sftp.remove(rname)

@skip_if_ci
def test_truncate_larger():
    '''test truncate, make file larger'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        try:
            sftp.remove(rname)
        except IOError:
            pass
        sftp.putfo(flo, rname)
        new_size = sftp.truncate(rname, 2*8192)
        assert new_size == 2*8192
        sftp.remove(rname)

@skip_if_ci
def test_truncate_same():
    '''test truncate, make file same size'''
    flo = BytesIO('*'*8192)
    rname = 'truncate.txt'
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        try:
            sftp.remove(rname)
        except IOError:
            pass
        sftp.putfo(flo, rname)
        new_size = sftp.truncate(rname, 8192)
        assert new_size == 8192
        sftp.remove(rname)

def test_truncate_ro():
    '''test truncate, against read-only server'''
    rname = 'readme.txt'
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with pytest.raises(IOError):
            _ = sftp.truncate(rname, 8192)

