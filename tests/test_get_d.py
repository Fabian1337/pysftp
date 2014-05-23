'''test pysftp.Connection.get_d - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

import pysftp

import shutil
from tempfile import mkdtemp

# pylint: disable = W0142
SFTP_PUBLIC = {'host':'68.226.78.92', 'username':'test',
               'password':'test1357', 'port':2222}


def test_get_d():
    '''test the get_d for remotepath is pwd '.' '''
    localpath = mkdtemp()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.get_d('.', localpath)

    checks = [([''], ['readme.txt',]),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)

def test_get_d_pathed():
    '''test the get_d for localpath, starting deeper then pwd '''
    localpath = mkdtemp()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.get_d('./pub/example', localpath)

    checks = [(['',],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)
