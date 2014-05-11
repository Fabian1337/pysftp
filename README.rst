pysftp
======

A simple interface to sftp.  based on zeth's ssh.py

Supports
--------
Tested on Python 2.7, 3.2, 3.3

.. image:: https://drone.io/bitbucket.org/dundeemt/pysftp/status.png
    :target: https://drone.io/bitbucket.org/dundeemt/pysftp/latest
    :alt: Build Status

Believed to support Python 3.4

Changes
-------

* 0.2.3

  * host code on pypi to keep pip happy
  * move code to bitbucket
  * enhance testing
  * README.rst and LICENSE named properly
  * cleaner error handling

* 0.2.2

  * additions

    * chdir(self, path) - change the current working directory on the remote
    * getcwd(self) - return the current working directory on the remote
    * listdir(self, path='.')return a list of files for the given path


* Project:  https://bitbucket.org/dundeemt/pysftp
* Download: https://pypi.python.org/pypi/pysftp