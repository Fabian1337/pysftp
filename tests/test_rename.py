'''test pysftp.Connection.rename - uses py.test'''

import os

from dhp.test import tempfile_containing

from common import SKIP_IF_CI


@SKIP_IF_CI
def test_rename(lsftp):
    '''test rename on remote'''
    contents = 'now is the time\nfor all good...'
    with tempfile_containing(contents=contents) as fname:
        base_fname = os.path.split(fname)[1]
        if base_fname in lsftp.listdir():
            lsftp.remove(base_fname)
        assert base_fname not in lsftp.listdir()
        lsftp.put(fname)
        lsftp.rename(base_fname, 'bob')
        rdirs = lsftp.listdir()
        assert 'bob' in rdirs
        assert base_fname not in rdirs
        lsftp.remove('bob')


# TODO
# def test_rename_ro(psftp):
#     '''test rename on a read-only server'''
#     with pytest.raises(IOError):
#         psftp.rename('/home/test/readme.txt', 'bob')
