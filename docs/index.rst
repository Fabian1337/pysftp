.. pysftp documentation master file, created by
   sphinx-quickstart on Sun May 11 08:53:24 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pysftp's documentation!
==================================
A simple interface to sftp.  based on zeth's ssh.py

Example
-------
.. code-block:: python

    import pysftp

    with pysftp.Connection('my.example.server') as sftp:
        with sftp.cd('public')              # temporarily chdir to public
            sftp.put('/my/local/filename')  # upload file to public/ on remote

        sftp.get_r('myfiles', '/backup')    # recursively copy myfiles/ to local



Supports
--------
Tested on Python 2.7, 3.2, 3.3

.. image:: https://drone.io/bitbucket.org/dundeemt/pysftp/status.png
    :target: https://drone.io/bitbucket.org/dundeemt/pysftp/latest
    :alt: Build Status

Believed to support Python 3.4

Additional Information
----------------------

* Project:  https://bitbucket.org/dundeemt/pysftp
* Download: https://pypi.python.org/pypi/pysftp
* Documentation: https://pysftp.rtfd.org/
* License: BSD

requirements
------------

  paramiko >= 1.7.7


Contents:

.. toctree::
   :maxdepth: 2

   cookbook
   pysftp
   changes
   contributing
   authors


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

