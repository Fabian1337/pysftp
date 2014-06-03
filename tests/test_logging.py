'''test pysftp.Connection logging param and CnOpts.log - uses py.test'''
from __future__ import print_function

# can't use fixtures here, as we need to get .close() to fire to clear the
# logging handlers while we are testing.
# pylint: disable = W0142
from common import *
import pytest

def test_depr_log_param(warnings_as_errors):
    '''test deprecation warning for Connection log parameter'''
    copts = SFTP_PUBLIC.copy()
    copts['log'] = True
    with pytest.raises(DeprecationWarning):
        with pysftp.Connection(**copts) as sftp:
            pass

def test_log_cnopt_user_file():
    '''test .logfile returns temp filename when CnOpts.log is set to True'''
    copts = SFTP_PUBLIC.copy()  # don't sully the module level variable
    cnopts = pysftp.CnOpts()
    cnopts.log = os.path.expanduser('~/my-logfile1.txt')
    copts['cnopts'] = cnopts
    with pysftp.Connection(**copts) as sftp:
        sftp.listdir()
        print(sftp.logfile, cnopts.log)
        assert sftp.logfile == cnopts.log
        assert os.path.exists(sftp.logfile)
        logfile = sftp.logfile
    # cleanup
    os.unlink(logfile)

def test_log_param_user_file():
    '''test .logfile returns temp filename when log param is set to True'''
    copts = SFTP_PUBLIC.copy()  # don't sully the module level variable
    copts['log'] = os.path.expanduser('~/my-logfile.txt')
    with pysftp.Connection(**copts) as sftp:
        print(sftp.logfile, copts['log'])
        assert sftp.logfile == copts['log']
        assert os.path.exists(sftp.logfile)
        logfile = sftp.logfile
    # cleanup
    os.unlink(logfile)

def test_log_param_false():
    '''test .logfile returns false when logging is set to false'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        print(SFTP_PUBLIC)
        assert sftp.logfile == False

def test_log_cnopts_explicit_false():
    '''test .logfile returns false when CnOpts.log is set to false'''
    copts = SFTP_PUBLIC.copy()  # don't sully the module level variable
    cnopts = pysftp.CnOpts()
    copts['cnopts'] = cnopts
    with pysftp.Connection(**copts) as sftp:
        print(SFTP_PUBLIC)
        assert sftp.logfile == False

def test_log_param_true():
    '''test .logfile returns temp filename when log param is set to True'''
    copts = SFTP_PUBLIC.copy()  # don't sully the module level variable
    copts['log'] = True
    with pysftp.Connection(**copts) as sftp:
        assert os.path.exists(sftp.logfile)
        # and we are not writing to a file named 'True'
        assert sftp.logfile != copts['log']
        logfile = sftp.logfile
    # cleanup
    os.unlink(logfile)

def test_log_cnopts_true():
    '''test .logfile returns temp filename when CnOpts.log is set to True'''
    copts = SFTP_PUBLIC.copy()  # don't sully the module level variable
    cnopts = pysftp.CnOpts()
    cnopts.log = True
    copts['cnopts'] = cnopts
    with pysftp.Connection(**copts) as sftp:
        assert os.path.exists(sftp.logfile)
        # and we are not writing to a file named 'True'
        assert sftp.logfile != cnopts.log
        logfile = sftp.logfile
    # cleanup
    os.unlink(logfile)
