'''test pysftp.Connection.get_r - uses py.test'''

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


def test_get_r():
    '''test the get_r for remotepath is pwd '.' '''
    localpath = mkdtemp()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.get_r('.', localpath)

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


def test_get_r_pwd():
    '''test the get_r for remotepath is pwd '/home/test' '''
    localpath = mkdtemp()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.get_r('/home/test', localpath)

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


def test_get_r_pathed():
    '''test the get_r for localpath, starting deeper then pwd '''
    localpath = mkdtemp()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.get_r('./pub/example', localpath)

    checks = [(['',], ['pub', ]),
              (['', 'pub'], ['example',]),
              (['', 'pub', 'example'],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)

def test_get_r_cdd():
    '''test the get_r for chdir('pub/example')'''
    localpath = mkdtemp()
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        sftp.chdir('pub/example')
        sftp.get_r('.', localpath)

    checks = [(['',],
               ['image01.jpg', 'image02.png', 'image03.gif', 'worksheet.xls']),
             ]
    for pth, fls in checks:
        assert sorted(os.listdir(os.path.join(localpath, *pth))) == fls

    # cleanup local
    shutil.rmtree(localpath)
