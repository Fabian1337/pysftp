pysftp
======

A simple interface to sftp.  based on zeth's ssh.py

changes
-------

* 0.2.3

  * host code on pypi to keep pip happy
  * implement a proper exception for lack of credentials
  * move code to bitbucket
  * enhance testing
  * README.rst and LICENSE named properly

* 0.2.2

  * additions

    * chdir(self, path) - change the current working directory on the remote
    * getcwd(self) - return the current working directory on the remote
    * listdir(self, path='.')return a list of files for the given path

