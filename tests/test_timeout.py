'''test pysftp.Connection.timeout - uses py.test'''

from common import skip_if_ci


@skip_if_ci
def test_timeout_getter(lsftp):
    '''test getting the timeout value'''
    # always starts at no timeout,
    assert lsftp.timeout is None


@skip_if_ci
def test_timeout_setter(lsftp):
    '''test setting the timeout value'''
    lsftp.timeout = 10.5
    assert lsftp.timeout == 10.5
    lsftp.timeout = None
    assert lsftp.timeout is None
