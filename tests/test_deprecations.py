'''these tests check for current deprecation messages'''
from __future__ import print_function

import warnings

# pylint: disable = W0142
from common import *


def test_depr_log_param():
    '''test deprecation warning for Connection log parameter'''
    with warnings.catch_warnings(record=True) as wrng:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        # Trigger a warning.
        copts = SFTP_PUBLIC.copy()
        copts['log'] = True
        sftp = pysftp.Connection(**copts)
        sftp.close
        # Verify some things
        assert len(wrng) == 1
        assert issubclass(wrng[-1].category, DeprecationWarning)
        assert "deprecated" in str(wrng[-1].message)
