'''test issues raised here if they don't fit else where - uses py.test'''

# pylint: disable = W0142
# pylint: disable=E1101
from common import *


@skip_if_ci
def test_issue_15(lsftp):
    '''chdir followed by execute doesn't occur in expected directory.'''
    hresults = lsftp.execute('pwd')
    lsftp.chdir('/home/test')
    assert hresults == lsftp.execute('pwd')
    # .exec operates independently of the current working directory .pwd
