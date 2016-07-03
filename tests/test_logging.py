'''test pysftp.Connection logging param and CnOpts.log - uses py.test'''
from __future__ import print_function
import os
import warnings

import pytest

from common import VFS, conn
import pysftp


def test_depr_log_param(sftpserver):
    '''test deprecation warning for Connection log parameter'''
    warnings.simplefilter('always')
    copts = conn(sftpserver)
    copts['log'] = True
    with sftpserver.serve_content(VFS):
        with pytest.warns(DeprecationWarning):  # pylint:disable=e1101
            with pysftp.Connection(**copts) as sftp:
                sftp.listdir()


def test_log_cnopt_user_file(sftpserver):
    '''test .logfile returns temp filename when CnOpts.log is set to True'''
    copts = conn(sftpserver)
    cnopts = pysftp.CnOpts()
    cnopts.log = os.path.expanduser('~/my-logfile1.txt')
    cnopts.hostkeys.load('sftpserver.pub')
    copts['cnopts'] = cnopts
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**copts) as sftp:
            sftp.listdir()
            assert sftp.logfile == cnopts.log
            assert os.path.exists(sftp.logfile)
            logfile = sftp.logfile
        # cleanup
        os.unlink(logfile)


def test_log_param_user_file(sftpserver):
    '''test .logfile returns temp filename when log param is set to True'''
    copts = conn(sftpserver)
    copts['log'] = os.path.expanduser('~/my-logfile.txt')
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**copts) as sftp:
            assert sftp.logfile == copts['log']
            assert os.path.exists(sftp.logfile)
            logfile = sftp.logfile
        # cleanup
        os.unlink(logfile)


def test_log_param_false(sftpserver):
    '''test .logfile returns false when logging is set to false'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            assert sftp.logfile is False


def test_log_cnopts_explicit_false(sftpserver):
    '''test .logfile returns false when CnOpts.log is set to false'''
    copts = conn(sftpserver)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys.load('sftpserver.pub')
    copts['cnopts'] = cnopts
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**copts) as sftp:
            assert sftp.logfile is False


def test_log_param_true(sftpserver):
    '''test .logfile returns temp filename when log param is set to True'''
    copts = conn(sftpserver)
    copts['log'] = True
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**copts) as sftp:
            assert os.path.exists(sftp.logfile)
            # and we are not writing to a file named 'True'
            assert sftp.logfile != copts['log']
            logfile = sftp.logfile
        # cleanup
        os.unlink(logfile)


def test_log_cnopts_true(sftpserver):
    '''test .logfile returns temp filename when CnOpts.log is set to True'''
    copts = conn(sftpserver)
    cnopts = pysftp.CnOpts()
    cnopts.log = True
    cnopts.hostkeys.load('sftpserver.pub')
    copts['cnopts'] = cnopts
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**copts) as sftp:
            assert os.path.exists(sftp.logfile)
            # and we are not writing to a file named 'True'
            assert sftp.logfile == cnopts.log
            logfile = sftp.logfile
        # cleanup
        os.unlink(logfile)
