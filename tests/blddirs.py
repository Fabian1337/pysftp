'''methods to build a known local directory structure, used in testing'''
import os
# pylint: disable = W0142

DIR_LIST = [('pub', ),
            ('pub', 'foo1'),
            ('pub', 'foo2'),
            ('pub', 'foo2', 'bar1')]
FILE_LIST = [('pub', 'read.me'),
             ('pub', 'make.txt'),
             ('pub', 'foo1', 'foo1.txt'),
             ('pub', 'foo2', 'foo2.txt'),
             ('pub', 'foo2', 'bar1', 'bar1.txt'),
            ]
def build_dir_struct(local_path):
    '''build directory structure'''
    for dparts in DIR_LIST:
        os.mkdir(os.path.join(local_path, *dparts))
    for fparts in FILE_LIST:
        with open(os.path.join(local_path, *fparts), 'wb') as fhndl:
            fhndl.write('*'*4096)

def remove_dir_struct(local_path):
    '''clean up directory struct'''
    for fparts in FILE_LIST:
        os.remove(os.path.join(local_path, *fparts))
    for dparts in reversed(DIR_LIST):
        os.rmdir(os.path.join(local_path, *dparts))

