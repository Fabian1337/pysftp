'''test pysftp.Connection.get - uses py.test'''

# pylint: disable = W0142
from common import *
from mock import Mock

def test_get():
    '''download a file'''
    sftp = pysftp.Connection(**SFTP_PUBLIC)
    with tempfile_containing('') as fname:
        sftp.get('readme.txt', fname)
        sftp.close()
        assert open(fname, 'rb').read()[0:9] == b'This SFTP'

def test_get_callback():
    '''test .get callback'''
    cback = Mock(return_value=None)
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('') as fname:
            result = sftp.get('readme.txt', fname, callback=cback)
            assert open(fname, 'rb').read()[0:9] == b'This SFTP'
    # verify callback was called more than once - usually a min of 2
    assert cback.call_count >= 2
    # unlike .put() nothing is returned from the operation
    assert result == None

def test_get_bad_remote():
    '''download a file'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        with tempfile_containing('') as fname:
            with pytest.raises(IOError):
                sftp.get('readme-not-there.txt', fname)
            assert open(fname, 'rb').read()[0:7] != b'Welcome'

# def test_get_glob():
#     '''try and use get a file with a pattern - Fails'''
#     with pysftp.Connection(**SFTP_PUBLIC) as sftp:
#         with tempfile_containing('') as fname:
#             with pytest.raises(IOError):
#                 sftp.get('*', fname)
