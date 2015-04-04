'''test pysftp.Connection.execute - uses py.test'''

# pylint: disable = W0142
from common import *
from dhp.VI import py_ver


# TODO
# def test_execute_simple_ro(psftp):
#     '''test execute simple on a read-only server '''
#     results = [b'This service allows sftp connections only.\n', ]
#     assert psftp.execute('ls') == results


@skip_if_ci
def test_execute_simple(lsftp):
    '''test execute simple'''
    if py_ver() == 2:
        type_check = basestring
    else:
        type_check = str

    results = lsftp.execute('ls')
    # confirm results are an iterable of strings (version dependent)
    for result in results:
        assert isinstance(result, type_check)
