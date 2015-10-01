'''test pysftp.Connection compression param - uses py.test'''
from __future__ import print_function
# these can not use fixtures as we need to set compression prior to the
# connection being made and fixtures are already active connections.

from common import skip_if_ci, SFTP_LOCAL
import pysftp


@skip_if_ci
def test_compression_default():
    '''test that a default connection does not have compression enabled'''
    with pysftp.Connection(**SFTP_LOCAL) as sftp:
        assert sftp.active_compression == ('none', 'none')


@skip_if_ci
def test_compression_enabled():
    '''test that compression=True results in compression enabled, assuming
    that the server supports compression'''
    copts = SFTP_LOCAL.copy()
    cnopts = pysftp.CnOpts()
    cnopts.compression = True
    copts['cnopts'] = cnopts
    with pysftp.Connection(**copts) as sftp:
        lcompress, rcompress = sftp.active_compression
        assert lcompress != 'none'
        assert rcompress != 'none'
