'''test pysftp.Connection.execute - uses py.test'''


from common import SKIP_IF_CI
from dhp.VI import py_ver


# TODO
# def test_execute_simple_ro(psftp):
#     '''test execute simple on a read-only server '''
#     results = [b'This service allows sftp connections only.\n', ]
#     assert psftp.execute('ls') == results


@SKIP_IF_CI
def test_execute_simple(lsftp):
    '''test execute simple'''
    if py_ver() == 2:
        type_check = basestring
    else:
        type_check = type(b'')

    results = lsftp.execute('ls')
    # confirm results are an iterable of strings (version dependent)
    for result in results:
        assert isinstance(result, type_check)
