'''test pysftp.Connection.open - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

from mock import Mock, call

# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}

def test_walktree_cbclass():
    '''test the walktree function with callbacks from a class'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        wtcb = pysftp.WTCallbacks()
        sftp.walktree('.',
                      fcallback=wtcb.file_cb,
                      dcallback=wtcb.dir_cb,
                      ucallback=wtcb.unk_cb)

    assert './pub/build/build01/build01a/build-results.txt' in wtcb.flist
    assert './readme.txt' in wtcb.flist
    assert len(wtcb.flist) > 3


    dlist = ['./pub', './pub/build', './pub/build/build01',
             './pub/build/build01/build01a', './pub/build/build01/build01b',
             './pub/build/build01/build01c', './pub/example', './pub/src',
             './pub/src/libs', './pub/src/media', './pub/src/tests']
    assert wtcb.dlist == dlist

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
    thecall = call('./pub/build/build01/build01a/build-results.txt')
    assert thecall in file_cb.mock_calls
    assert file_cb.call_count > 3
    # check calls to the directory callback
    assert [call('./pub'),
            call('./pub/build'),
            call('./pub/build/build01'),
            call('./pub/build/build01/build01a'),
            call('./pub/build/build01/build01b'),
            call('./pub/build/build01/build01c'),
            call('./pub/example'),
            call('./pub/src'),
            call('./pub/src/libs'),
            call('./pub/src/media'),
            call('./pub/src/tests')] == dir_cb.mock_calls
    # check calls to the unknown callback
    assert [] == unk_cb.mock_calls
