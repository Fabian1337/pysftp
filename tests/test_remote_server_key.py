'''test pysftp.Connection.remote_server_key - uses py.test'''
from __future__ import print_function
import os

from paramiko.hostkeys import HostKeys
import pytest

from common import VFS, conn
import pysftp


def test_cd_none(sftpserver):
    '''test .cd with None'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as sftp:
            rsk = sftp.remote_server_key
            print(type(rsk))
            print(dir(rsk))
            print('host:', sftpserver.host)
            print('keytype:', rsk.get_name())
            print('base64:', rsk.get_base64())
            hks = HostKeys()
            hks.add(hostname=sftpserver.host,
                    keytype=rsk.get_name(),
                    key=rsk)
            hks.save('sftpserver.pub')
            assert False
