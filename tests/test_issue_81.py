"""test issue #81, download a huge file stalls."""

from __future__ import print_function
import os

from common import SKIP_IF_CI


@SKIP_IF_CI     # required when using the local sftp server - lsftp
def test_issue_81_get(lsftp):
    '''get a 1GB file'''
    # dd if=/dev/urandom of=hugefile.random bs=1048576 count=1000
    # now the test phase
    huge_file = 'hugefile.random'
    huge_file_size = 1048576000
    if os.path.exists(huge_file):
        os.remove(huge_file)
    with lsftp.cd('huge'):
        lsftp.get('hugefile.random')
    assert os.path.getsize(huge_file) == huge_file_size
