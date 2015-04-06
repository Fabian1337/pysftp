'''common setup code for tests'''

# the following 3 lines let py.test find the module
import os
import sys
import warnings

from dhp.test import tempfile_containing
import pytest

MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp       # noqa


# pytest-sftpserver plugin information
SFTP_INTERNAL = {'host': 'localhost', 'username': 'user', 'password': 'pw'}
# used if ptest-sftpserver plugin does not support what we are testing
SFTP_LOCAL = {'host': 'localhost', 'username': 'test', 'password': 'test1357'}

# can only reach public, read-only server from CI platform, only test locally
# if environment variable CI is set  to something to disable local tests
# the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '') > '', reason='Not Local')
# try:
#     stars8192 = bytes('*'*8192)
# except TypeError:
stars8192 = '*'*8192


@pytest.fixture
def warnings_as_errors(request):
    '''make warnings jump out as errors so they are simpler to test'''
    warnings.simplefilter('error')

    request.addfinalizer(lambda *args: warnings.resetwarnings())


def conn(sftpsrv):
    """return a dictionary holding argument info for the pysftp client"""
    return {'host': sftpsrv.host, 'port': sftpsrv.port, 'username': 'user',
            'password': 'pw', 'default_path': '/home/test'}

# filesystem served by pytest-sftpserver plugin
VFS = {
    'home': {
        'test': {
            'pub': {
                'make.txt': "content of make.txt",
                'foo1': {
                        'foo1.txt': 'content of foo1.txt',
                        'image01.jpg': 'data for image01.jpg'
                },
                'foo2': {
                        'foo2.txt': 'content of foo2.txt',
                        'bar1': {
                            'bar1.txt': 'contents bar1.txt'
                        }
                }
            },
            'read.me': 'contents of read.me',
        }
    }
}
