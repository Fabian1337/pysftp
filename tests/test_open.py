'''test pysftp.Connection.open - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

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


def test_open_read():
    '''test the open function'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        rfile = sftp.open('readme.txt')
        contents = rfile.read()
        rfile.close()
    assert contents[0:7] == b'Welcome'

def test_open_read_with():
    '''test the open function in a with statment'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with sftp.open('readme.txt') as rfile:
            contents = rfile.read()
    assert contents[0:7] == b'Welcome'
