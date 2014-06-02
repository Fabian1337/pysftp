'''test pysftp.Connection compression param - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *


def test_compression_default():
    '''test that a default connection does not have compression enabled'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        assert sftp.active_compression == ('none', 'none')


def test_compression_enabled():
    '''test that compression=True results in compression enabled, assuming
    that the server supports compression'''
    copts = SFTP_PUBLIC.copy()
    cnopts = pysftp.CnOpts()
    cnopts.compression = True
    copts['cnopts'] = cnopts
    with pysftp.Connection(**copts) as sftp:
        lcompress, rcompress = sftp.active_compression
        assert lcompress != 'none'
        assert rcompress != 'none'


