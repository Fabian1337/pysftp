pysftp
======

A simple interface to sftp.  based on zeth's ssh.py

Example
-------
::

    import pysftp

    with pysftp.Connection('my.example.server') as sftp:
        sftp.put('/my/local/filename', '/my/remote/filename')
        sftp.get('the-file.txt')


Supports
--------
Tested on Python 2.7, 3.2, 3.3

.. image:: https://drone.io/bitbucket.org/dundeemt/pysftp/status.png
    :target: https://drone.io/bitbucket.org/dundeemt/pysftp/latest
    :alt: Build Status

Believed to support Python 3.4

* Project:  https://bitbucket.org/dundeemt/pysftp
* Download: https://pypi.python.org/pypi/pysftp
* Documentation: http://pysftp.rtfd.org/

