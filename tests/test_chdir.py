'''test pysftp.Connection.chdir - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *

def test_chdir_bad_dir(psftp):
    '''try to chdir() to a non-existing remote dir'''
    with pytest.raises(IOError):
        psftp.chdir('i-dont-exist')

