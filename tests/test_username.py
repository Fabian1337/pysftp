'''test username parameter'''
# pylint: disable=W0142,W0212
from __future__ import print_function
import os

import pytest

from common import VFS, conn
import pysftp


def test_username_specified(sftpserver):
    '''test specifying username as parameter'''
    with sftpserver.serve_content(VFS):
        params = conn(sftpserver)
        params['username'] = 'bob'
        with pysftp.Connection(**params) as sftp:
            assert sftp._username == params['username']


def test_username_from_environ(sftpserver):
    '''test reading username from $LOGNAME environment variable.'''
    username = 'bob'
    hold_logname = os.environ.get('LOGNAME')
    os.environ['LOGNAME'] = username
    with sftpserver.serve_content(VFS):
        params = conn(sftpserver)
        del params['username']
        with pysftp.Connection(**params) as sftp:
            if hold_logname is not None:
                os.environ['LOGNAME'] = hold_logname
            assert sftp._username == username


def test_no_username_raises_err(sftpserver):
    '''test No username raises CredentialException.'''
    hold_logname = os.environ.get('LOGNAME')
    del os.environ['LOGNAME']
    with sftpserver.serve_content(VFS):
        params = conn(sftpserver)
        del params['username']
        with pytest.raises(pysftp.CredentialException):
            pysftp.Connection(**params)
    if hold_logname is not None:
        os.environ['LOGNAME'] = hold_logname
