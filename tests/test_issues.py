'''test issues raised here if they don't fit else where - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


def test_issue_15(psftp):
    '''chdir followed by execute doesn't occur in expected directory.'''
    hresults = psftp.execute('pwd')
    psftp.chdir('pub')
    assert hresults == psftp.execute('pwd')
    # .exec operates independently of the current working directory .pwd
