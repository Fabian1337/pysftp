'''test pysftp.Connection.get_r - uses py.test'''

# pylint: disable = W0142
from common import *
from tempfile import mkdtemp
import shutil


def test_get_r(psftp):
    '''test the get_r for remotepath is pwd '.' '''
    psftp.cwd('/home/test')
    localpath = mkdtemp()
    psftp.get_r('.', localpath)

    checks = [([''], ['pub', 'readme.sym', 'readme.txt']),
              (['', 'pub'], ['build', 'example', 'src']),
              (['', 'pub', 'build'], ['build01']),
              (['', 'pub', 'build', 'build01'],
               ['build01a', 'build01b', 'build01c']),
              (['', 'pub', 'build', 'build01', 'build01a'],
               ['build-results.txt',]),
              (['', 'pub', 'build', 'build01', 'build01b'], []),
              (['', 'pub', 'build', 'build01', 'build01c'],
               ['build-results.txt',]),
              (['', 'pub', 'example'],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
              (['', 'pub', 'src'],
               ['helpers.py', 'libs', 'main.py', 'media', 'tests']),
              (['', 'pub', 'src', 'libs'], ['do-nothing.library',]),
              (['', 'pub', 'src', 'media'], ['favicon.ico', 'logo.jpg']),
              (['', 'pub', 'src', 'tests'],
               ['test01.py', 'test02.py', 'test03.py']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)


def test_get_r_pwd(psftp):
    '''test the get_r for remotepath is pwd '/home/test' '''
    psftp.cwd('/home/test')
    localpath = mkdtemp()
    psftp.get_r('/home/test', localpath)

    checks = [(['',], ['home', ]),
              (['', 'home',], ['test',]),
              (['', 'home', 'test'], ['pub', 'readme.sym', 'readme.txt']),
              (['', 'home', 'test', 'pub'], ['build', 'example', 'src']),
              (['', 'home', 'test', 'pub', 'build'], ['build01']),
              (['', 'home', 'test', 'pub', 'build', 'build01'],
               ['build01a', 'build01b', 'build01c']),
              (['', 'home', 'test', 'pub', 'build', 'build01', 'build01a'],
               ['build-results.txt',]),
              (['', 'home', 'test', 'pub', 'build', 'build01', 'build01b'], []),
              (['', 'home', 'test', 'pub', 'build', 'build01', 'build01c'],
               ['build-results.txt',]),
              (['', 'home', 'test', 'pub', 'example'],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
              (['', 'home', 'test', 'pub', 'src'],
               ['helpers.py', 'libs', 'main.py', 'media', 'tests']),
              (['', 'home', 'test', 'pub', 'src', 'libs'],
               ['do-nothing.library',]),
              (['', 'home', 'test', 'pub', 'src', 'media'],
               ['favicon.ico', 'logo.jpg']),
              (['', 'home', 'test', 'pub', 'src', 'tests'],
               ['test01.py', 'test02.py', 'test03.py']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)


def test_get_r_pathed(psftp):
    '''test the get_r for localpath, starting deeper then pwd '''
    psftp.cwd('/home/test')
    localpath = mkdtemp()
    psftp.get_r('./pub/example', localpath)

    checks = [(['',], ['pub', ]),
              (['', 'pub'], ['example',]),
              (['', 'pub', 'example'],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)

def test_get_r_cdd(psftp):
    '''test the get_r for chdir('pub/example')'''
    psftp.cwd('/home/test')
    localpath = mkdtemp()
    psftp.chdir('pub/example')
    psftp.get_r('.', localpath)

    checks = [(['',],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)
