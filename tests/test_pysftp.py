'''test pysftp module - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp


def test_connection_good():
    '''connect to a public sftp server'''
    sftp = pysftp.Connection(host='test.rebex.net',
                             username='demo',
                             password='password')
    sftp.close()


def test_connection_local():
    '''try and connect to localhost'''
    sftp = pysftp.Connection('localhost')
    sftp.close()


def test_connection_bad():
    '''attempt connection to a non-existing server'''
    try:
        sftp = pysftp.Connection('nota.realserver.pri')
        assert False
    except:
        assert True

