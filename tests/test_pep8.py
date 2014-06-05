'''test pysftp module, setup.py and tests - uses py.test'''
import pep8


def test_pep8():
    '''pep8 check the source'''
    # list the specific files or directories to check, directories are recursed
    paths = ['pysftp.py', 'setup.py', 'tests']
    p8c = pep8.StyleGuide()
    report = p8c.check_files(paths=paths)
    report.print_statistics()
    assert report.get_count() == 0
