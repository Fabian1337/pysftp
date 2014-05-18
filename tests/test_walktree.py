'''test pysftp.Connection.open - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

from mock import Mock, call
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


class WTCallbacks(object):
    '''create an object to house the callbacks'''
    def __init__(self):
        '''set instance vars'''
        self.flist = []
        self.dlist = []
        self.ulist = []

    def file_cb(self, pathname):
        '''called for regular files'''
        self.flist.append(pathname)

    def dir_cb(self, pathname):
        '''called for directories'''
        self.dlist.append(pathname)

    def unk_cb(self, pathname):
        '''called for unknown file types'''
        self.ulist.append(pathname)

def test_walktree_cbclass():
    '''test the walktree function with callbacks from a class'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        wtcb = WTCallbacks()
        sftp.walktree('.',
                      fcallback=wtcb.file_cb,
                      dcallback=wtcb.dir_cb,
                      ucallback=wtcb.unk_cb)

    assert u'./pub/example/ConsoleClient.png' in wtcb.flist
    assert u'./readme.txt' in wtcb.flist
    assert len(wtcb.flist) > 3

    assert wtcb.dlist == [u'./pub', u'./pub/example', u'./pub/test']

    assert wtcb.ulist == []

def test_walktree_cbmock():
    '''test the walktree function, with mocked callbacks (standalone functions)
    '''
    file_cb = Mock(return_value=None)
    dir_cb = Mock(return_value=None)
    unk_cb = Mock(return_value=None)

    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.walktree('.',
                      fcallback=file_cb,
                      dcallback=dir_cb,
                      ucallback=unk_cb)
    # check calls to the file callback
    file_cb.assert_called_with(u'./readme.txt')
    assert call(u'./pub/example/ConsoleClient.png') in file_cb.mock_calls
    assert file_cb.call_count > 3
    # check calls to the directory callback
    assert [call(u'./pub'),
            call(u'./pub/example'),
            call(u'./pub/test')] == dir_cb.mock_calls
    # check calls to the unknown callback
    assert [] == unk_cb.mock_calls
