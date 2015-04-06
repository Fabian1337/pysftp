"""use the cd contextmanager prior to paramiko establishing a directory
location"""

from __future__ import print_function

# pylint: disable = W0142
from common import VFS, conn, pysftp


def test_issue_65(sftpserver):
    '''using the .cd() context manager prior to setting a dir via chdir
    causes an error'''
    with sftpserver.serve_content(VFS):
        cn = conn(sftpserver)
        cn['default_path'] = None  # don't call .chdir by setting default_path
        with pysftp.Connection(**cn) as sftp:
            assert sftp.getcwd() is None
            with sftp.cd('/home/test/pub'):
                sftp.listdir('.')
            assert sftp.getcwd() is None
