'''test pysftp.Connection.chdir - uses py.test'''

import pytest

from common import VFS, conn
import pysftp


def test_chdir_bad_dir(sftpserver):
    '''try to chdir() to a non-existing remote dir'''
    with sftpserver.serve_content(VFS):
        with pysftp.Connection(**conn(sftpserver)) as psftp:
            with pytest.raises(IOError):
                psftp.chdir('i-dont-exist')
