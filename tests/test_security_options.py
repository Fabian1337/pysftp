'''test pysftp.Connection compression param - uses py.test'''
from __future__ import print_function

# pylint: disable = W0142
from common import *

def test_security_options():
    '''test the security_options property has expected attributes and that
    they are tuples'''
    with pysftp.Connection(**SFTP_PUBLIC) as sftp:
        secopts = sftp.security_options
    for attr in ['ciphers', 'compression', 'digests', 'kex', 'key_types']:
        assert hasattr(secopts, attr)
        assert isinstance(getattr(secopts, attr), tuple)

