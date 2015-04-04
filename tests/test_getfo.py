'''test pysftp.Connection.getfo - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *
from io import BytesIO
from mock import Mock


def test_getfo_flo(sftpserver):
    '''test getfo to a file-like object'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            flo = BytesIO()
            psftp.chdir('/pub')
            num_bytes = psftp.getfo('make.txt', flo)

            assert flo.getvalue() == b'content of make.txt'
            assert num_bytes == len(flo.getvalue())


def test_getfo_callback(sftpserver):
    '''test getfo callback'''
    with sftpserver.serve_content(CONTENT):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            flo = BytesIO()
            cback = Mock(return_value=None)
            psftp.chdir('/pub')
            psftp.getfo('make.txt', flo, callback=cback)

            assert cback.call_count >= 2
