'''setup for package'''

from setuptools import setup

with open('README.rst') as h_readme:
    LONG_DESCRIPTION = h_readme.read()

with open('docs/changes.rst') as h_readme:
    BUF = h_readme.read()
    BUF = BUF.replace('``', '$')        # protect code markers
    for xref in [':meth:', ':attr:', ':class:', ':func:']:
        BUF = BUF.replace(xref, '')     # remove xrefs
    # BUF = BUF.replace(':meth:', '')     # remove links
    # BUF = BUF.replace(':attr:', '')
    # BUF = BUF.replace(':class:', '')
    # BUF = BUF.replace(':func:', '')
    BUF = BUF.replace('`', '``')        # replace refs with code markers
    BUF = BUF.replace('$', '``')        # restore existing code markers
LONG_DESCRIPTION += BUF

DESCRIPTION = "A friendly face on SFTP"

setup(
    name="pysftp",
    version="0.2.6",

    py_modules=['pysftp'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['paramiko>=1.7.7'],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['LICENSE.txt', '*.txt', '*.rst'],
    # },

    # metadata for upload to PyPI
    author="Jeff Hinrichs",
    author_email="jeffh@dundeemt.com",
    description=DESCRIPTION,
    license="BSD",
    keywords="sftp ssh ftp internet",
    url="https://bitbucket.org/dundeemt/pysftp",   # project home page
    long_description=LONG_DESCRIPTION,
    platforms=['any'],
    download_url='https://pypi.python.org/pypi/pysftp',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

)
