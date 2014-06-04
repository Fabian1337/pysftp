'''test pysftp.Connection.timeout - uses py.test'''

# pylint: disable = W0142
from common import *


def test_timeout_getter(psftp):
    '''test getting the timeout value'''
    # always starts at no timeout,
    assert psftp.timeout is None


def test_timeout_setter(psftp):
    '''test setting the timeout value'''
    psftp.timeout = 10.5
    assert psftp.timeout == 10.5
    psftp.timeout = None
    assert psftp.timeout is None
