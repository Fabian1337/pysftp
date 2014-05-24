'''test pysftp.Connection.listdir - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

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


