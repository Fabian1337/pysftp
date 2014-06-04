'''test pysftp.Connection.getfo - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from io import BytesIO
from mock import Mock


def test_getfo_flo(psftp):
    '''test getfo to a file-like object'''
    flo = BytesIO()
    psftp.chdir('/home/test')
    num_bytes = psftp.getfo('readme.txt', flo)

    assert flo.getvalue()[0:9] == b'This SFTP'
    assert num_bytes == len(flo.getvalue())


def test_getfo_callback(psftp):
    '''test getfo callback'''
    flo = BytesIO()
    cback = Mock(return_value=None)
    psftp.chdir('/home/test')
    psftp.getfo('readme.txt', flo, callback=cback)

    assert cback.call_count >= 2
