'''test pysftp.Connection ciphers param and CnOpts.ciphers - uses py.test'''
from __future__ import print_function

# these can not use fixtures as we need to set ciphers prior to the connection
# being made and fixtures are already active connections.
# pylint: disable = W0142
from common import *
import pytest


@skip_if_ci
def test_depr_ciphers_param(warnings_as_errors):
    '''test deprecation warning for Connection cipher parameter'''
    copts = SFTP_LOCAL.copy()
    copts['ciphers'] = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc',
                        'arcfour256')
    with pytest.raises(DeprecationWarning):
        with pysftp.Connection(**copts) as sftp:
            pass


@skip_if_ci
def test_connection_ciphers_param():
    '''test the ciphers parameter portion of the Connection'''
    ciphers = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc', 'arcfour256')
    copts = SFTP_LOCAL.copy()  # don't sully the module level variable
    copts['ciphers'] = ciphers
    assert copts != SFTP_LOCAL
    with pysftp.Connection(**copts) as sftp:
        rslt = sftp.listdir()
        assert len(rslt) > 1


@skip_if_ci
def test_connection_ciphers_cnopts():
    '''test the CnOpts.ciphers portion of the Connection'''
    ciphers = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc', 'arcfour256')
    copts = SFTP_LOCAL.copy()  # don't sully the module level variable
    cnopts = pysftp.CnOpts()
    cnopts.ciphers = ciphers
    copts['cnopts'] = cnopts
    assert copts != SFTP_LOCAL
    with pysftp.Connection(**copts) as sftp:
        rslt = sftp.listdir()
        assert len(rslt) > 1


@skip_if_ci
def test_active_ciphers():
    '''test that method returns a tuple of strings, that show ciphers used'''
    ciphers = ('aes256-ctr', 'blowfish-cbc', 'aes256-cbc', 'arcfour256')
    copts = SFTP_LOCAL.copy()  # don't sully the module level variable
    cnopts = pysftp.CnOpts()
    cnopts.ciphers = ciphers
    copts['cnopts'] = cnopts
    with pysftp.Connection(**copts) as sftp:
        local_cipher, remote_cipher = sftp.active_ciphers
    assert local_cipher in ciphers
    assert remote_cipher in ciphers
