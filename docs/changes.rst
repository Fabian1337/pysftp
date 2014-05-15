Change Log
----------


* 0.2.5 (dev)

  * added ciphers parameter to Connection object
  * added .active_ciphers method to return local and remote cipher in use
  * added .security_options, from where you can get available ciphers, among other information
  * enhanced logging, and added documentation and tests

* 0.2.4 (current, released 2014-05-13)

  * pysftp.Connection can be used in a `with` statement
  * add .remove() method
  * added support for callback and confirm params to .put() method
  * added support for callback on .get() method
  * added support for .open()
  * fixed password bug and now differentiates between an empty string and None
  * added support for paramiko.AgentKey to be passed in as the private_key for Connection
  * added support for .mkdir()
  * added support for .rmdir()
  * added support for .stat() and .lstat()
  * added helper function, st_mode_to_int,to convert the st_mode value back into a common integer representation
  * added .getfo() method
  * added .putfo() method

* 0.2.3 (released 2014-05-10)

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
