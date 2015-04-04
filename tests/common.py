'''common setup code for tests'''

# the following 3 lines let py.test find the module
import sys
import os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')
import warnings     # noqa

import pysftp       # noqa

import pytest       # noqa
from dhp.test import tempfile_containing    # noqa


# pylint: disable=E1101
if os.path.exists('/home/jlh/projects/pysftp'):
    SFTP_PUBLIC = {'host': 'srv01.dundeemt.pri', 'username': 'test',
                   'password': 'test1357'}
else:
    SFTP_PUBLIC = {'host': '174.74.39.157', 'username': 'test',
                   'password': 'test1357', 'port': 2222}
# SFTP_PUBLIC = {'host':'test.rebex.net', 'username':'demo',
#                'password':'password'}
SFTP_LOCAL = {'host': 'localhost', 'username': 'test', 'password': 'test1357'}

SFTP_INTERNAL = {'host': 'localhost', 'username': 'user', 'password': 'pw'}
# can only reach public, read-only server from CI platform, only test locally
# if environment variable CI is set  to something to disable local tests
# the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '') > '', reason='Not Local')


@pytest.fixture
def warnings_as_errors(request):
    '''make warnings jump out as errors so they are simpler to test'''
    warnings.simplefilter('error')

    request.addfinalizer(lambda *args: warnings.resetwarnings())


def conn(sftpsrv):
    """return a dictionary holding connection info for the pysftp client"""
    return {'host': sftpsrv.host, 'port': sftpsrv.port, 'username': 'user',
            'password': 'pw'}

CONTENT = {'pub': {
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
