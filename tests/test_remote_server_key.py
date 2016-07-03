'''test pysftp.Connection.remote_server_key - uses py.test'''
from __future__ import print_function

from paramiko.hostkeys import HostKeys
from paramiko.rsakey import RSAKey
import pytest

from common import VFS, conn
import pysftp
from pysftp import HostKeysException, SSHException


def test_remote_server_key(sftpserver):
    '''test .remote_server_key property'''
    with sftpserver.serve_content(VFS):
        this_conn = conn(sftpserver)
        this_conn['cnopts'].hostkeys = None     # turn-off hostkey verification
        with pysftp.Connection(**this_conn) as sftp:
            rsk = sftp.remote_server_key
            hks = HostKeys()
            hks.add(hostname=sftpserver.host,
                    keytype=rsk.get_name(),
                    key=rsk)
            hks.save('sftpserver.pub')


def test_cnopts_no_knownhosts():
    '''test setting knownhosts to a non-existant file'''
    with pytest.warns(UserWarning):     # pylint:disable=e1101
        pysftp.CnOpts(knownhosts='i-m-not-there')


def test_cnopts_bad_knownhosts():
    '''test setting knownhosts to a not understood file'''
    with pytest.raises(HostKeysException):
        pysftp.CnOpts(knownhosts='tox.ini')


def test_hostkey_not_found():
    '''test that an exception is raised when no host key is found'''
    cnopts = pysftp.CnOpts(knownhosts='sftpserver.pub')
    with pytest.raises(SSHException):
        cnopts.get_hostkey(host='missing-server')


def test_hostkey_returns_pkey():
    '''test the finding a matching host key returns a PKey'''
    cnopts = pysftp.CnOpts(knownhosts='sftpserver.pub')
    assert isinstance(cnopts.get_hostkey('127.0.0.1'), RSAKey)
