Change Log
----------


* 0.2.8 (dev)

  * in progress


* 0.2.7 (current, released 2014-05-24)

  * created :meth:`.walktree`, recursively walk, depth first, a remote directory structure.  Used as the base of :meth:`.get_r`. See tests/test_walktree.py for examples.
  * added :meth:`.unlink` as synonym for :meth:`.remove`
  * added :meth:`.normalize`
  * created :meth:`.get_r` to recursively copy remote directories to a local path
  * created :attr:`.pwd` to return the current working directory
  * created :meth:`.cwd` as synonym for :meth:`.chdir`
  * modified :meth:`.listdir` to return a sorted list instead of an arbitrary one
  * added :meth:`.readlink`, always returns an absolute path
  * created :meth:`.get_d` to copy the remote directory to a local path (non-recursive)
  * added :attr:`.timeout` to set the read/write timeout of the underlying channel for pending read/write ops
  * added :meth:`.listdir_attr`, wrapper for paramiko method
  * added :meth:`.truncate`, method returns the new file size
  * improved DRY'ness of test suite

* 0.2.6 (released 2014-05-17)

  * added ``preserve_mtime`` parameter to :meth:`.put`, optionally updates the remote file's st_mtime to match the local file.
  * added ``preserve_mtime`` parameter to :meth:`.get`, optionally updates the local file's st_mtime to match the remote file
  * added :meth:`.exists` and :meth:`.lexists`, use :meth:`.stat` and :meth:`.lstat` respectively
  * added :meth:`.symlink`
  * created :meth:`.isdir`, :meth:`.isfile`, :meth:`.makedirs`
  * added :meth:`.chmod`
  * added :meth:`.chown`
  * added :attr:`.sftp_client` which exposes underlying, active ``SFTPClient`` object for advance use

* 0.2.5 (released 2014-05-15)

  * added ``ciphers`` parameter to :class:`.Connection` object
  * added :attr:`.active_ciphers` to return local and remote cipher in use
  * added :attr:`.security_options`, where you can get available ciphers, among other information
  * enhanced logging, and added documentation and tests

* 0.2.4 (released 2014-05-13)

  * :class:`.Connection` can be used in a ``with`` statement
  * add :meth:`.remove`
  * added support for callback and confirm params to :meth:`.put`
  * added support for callback on :meth:`.get`
  * added support for :meth:`.open`
  * fixed password bug and now differentiates between an empty string and None
  * added support for ``paramiko.AgentKey`` to be passed in as the ``private_key`` for Connection
  * added support for :meth:`.mkdir`
  * added support for :meth:`.rmdir`
  * added support for :meth:`.stat` and :meth:`.lstat`
  * added helper function, :func:`.st_mode_to_int`,to convert the ``st_mode`` value back into a common integer representation
  * added :meth:`.getfo`
  * added :meth:`.putfo`

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
