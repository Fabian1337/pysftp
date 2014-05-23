'''test pysftp.Connection.execute - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pytest

import pysftp


# pylint: disable=E1101
# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}
SFTP_LOCAL = {'host':'localhost', 'username':'test', 'password':'test1357'}
 #can only reach public, read-only server from CI platform, only test locally
 # if environment variable CI is set  to something to disable local tests
 # the CI env var is set to true by both drone-io and travis
skip_if_ci = pytest.mark.skipif(os.getenv('CI', '')>'', reason='Not Local')


def test_execute_simple_ro():
    '''test execute simple on a read-only server '''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        # always starts at no timeout,
        results = [b'This service allows sftp connections only.\n',]
        assert sftp.execute('ls') == results

@skip_if_ci
def test_execute_simple():
    '''test execute simple'''
    if sys.version_info[0] == 2:
        type_check = basestring
    else:
        type_check = str

    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        # always starts at no timeout,
        results = sftp.execute('ls')
        for result in results:
            assert isinstance(result, type_check)

