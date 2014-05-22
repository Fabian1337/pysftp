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


def test_walktree_cbclass():
    '''test the walktree function with callbacks from a class'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        wtcb = pysftp.WTCallbacks()
        sftp.walktree('.',
                      fcallback=wtcb.file_cb,
                      dcallback=wtcb.dir_cb,
                      ucallback=wtcb.unk_cb)

    assert './pub/example/ConsoleClient.png' in wtcb.flist
    assert './readme.txt' in wtcb.flist
    assert len(wtcb.flist) > 3

    assert wtcb.dlist == ['./pub', './pub/example', './pub/test']

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
    file_cb.assert_called_with('./readme.txt')
    assert call('./pub/example/ConsoleClient.png') in file_cb.mock_calls
    assert file_cb.call_count > 3
    # check calls to the directory callback
    assert [call('./pub'),
            call('./pub/example'),
            call('./pub/test')] == dir_cb.mock_calls
    # check calls to the unknown callback
    assert [] == unk_cb.mock_calls
