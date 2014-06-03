'''test pysftp.Connection.get_d - uses py.test'''

# pylint: disable = W0142
from common import *
from tempfile import mkdtemp
import shutil


def test_get_d(psftp):
    '''test the get_d for remotepath is pwd '.' '''
    psftp.cd('~')
    localpath = mkdtemp()
    psftp.get_d('.', localpath)

    checks = [([''], ['readme.txt',]),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)

def test_get_d_pathed(psftp):
    '''test the get_d for localpath, starting deeper then pwd '''
    psftp.cd('~')
    localpath = mkdtemp()
    psftp.get_d('./pub/example', localpath)

    checks = [(['',],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)
