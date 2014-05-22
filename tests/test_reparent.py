'''test pysftp.reparent(newparent, oldpath) - uses py.test'''

# the following 3 lines let py.test find the module
import sys, os
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')

from pysftp import reparent


def test_reparent_dotted():
    '''test the reparent if oldpath beings with '.' '''
    newparent = '/tmp/fuzzy'
    oldpath = '.'
    assert reparent(newparent, oldpath) == os.path.join(newparent, oldpath)


def test_reparent_with_ending_slash():
    '''test the reparent if oldpath beings with '.' '''
    newparent = '/tmp/fuzzy/'
    oldpath = '.'
    assert reparent(newparent, oldpath) == os.path.join(newparent, oldpath)

def test_reparent_root():
    '''test the reparent if oldpath beings with '.' '''
    newparent = '/tmp/fuzzy'
    oldpath = '/pub'
    assert reparent(newparent, oldpath) == os.path.join(newparent,
                                                        '.' + oldpath)

def test_reparent_dotted_root():
    '''test the reparent if oldpath beings with '.' '''
    newparent = '/tmp/fuzzy'
    oldpath = './pub/example'
    assert reparent(newparent, oldpath) == os.path.join(newparent, oldpath)
