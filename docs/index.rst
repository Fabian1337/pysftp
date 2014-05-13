.. pysftp documentation master file, created by
   sphinx-quickstart on Sun May 11 08:53:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pysftp's documentation!
==================================
A simple interface to sftp.  based on zeth's ssh.py

Example
-------
.. code:: python

    import pysftp
    with pysftp.Connection('my.example.server') as sftp:
        sftp.put('/my/local/filename', '/my/remote/filename')


Supports
--------
Tested on Python 2.7, 3.2, 3.3

.. image:: https://drone.io/bitbucket.org/dundeemt/pysftp/status.png
    :target: https://drone.io/bitbucket.org/dundeemt/pysftp/latest
    :alt: Build Status

Believed to support Python 3.4

* Project:  https://bitbucket.org/dundeemt/pysftp
* Download: https://pypi.python.org/pypi/pysftp
* Documentation: https://pysftp.rtfd.org/

requirements
------------

  paramiko >= 1.7.4


Contents:

.. toctree::
   :maxdepth: 2

   pysftp
   changes
   contributing
   authors


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

