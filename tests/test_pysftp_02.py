'''test pysftp module - set 2 - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

# from io import BytesIO
from time import sleep

import pysftp

from dhp.test import tempfile_containing
# from mock import Mock, call
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

@skip_if_ci
def test_put_preserve_mtime():
    '''test that m_time is preserved from local to remote, when put'''
    with tempfile_containing(contents=8192*'*') as fname:
        base_fname = os.path.split(fname)[1]
        base = os.stat(fname)
        with pysftp.Connection(**SFTP_LOCAL) as sftp:
            result1 = sftp.put(fname, preserve_mtime=True)
            sleep(2)
            result2 = sftp.put(fname, preserve_mtime=True)
            # clean up
            sftp.remove(base_fname)
    # see if times are modified
    # assert base.st_atime == result1.st_atime
    assert base.st_mtime == result1.st_mtime
    # assert result1.st_atime == result2.st_atime
    assert result1.st_mtime == result2.st_mtime
