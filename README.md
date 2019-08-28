pysftp
======

A simple interface to SFTP.  The module offers high level abstractions and
task based routines to handle your SFTP needs.  Checkout the Cook Book, in the
docs, to see what pysftp can do for you.

Example
-------

Added `auto_add_key`:
based on [verify-host-key-with-pysftp](https://stackoverflow.com/questions/38939454/verify-host-key-with-pysftp), [use-paramiko-autoaddpolicy-with-pysftp](https://stackoverflow.com/questions/53666106/use-paramiko-autoaddpolicy-with-pysftp)

>*Do not set cnopts.hostkeys = None (as the most upvoted answer shows), unless you do not care about security. You lose a protection >against Man-in-the-middle attacks by doing so.'*

>*Though for an absolute security, you should not retrieve the host key remotely, as you cannot be sure, if you are not being attacked already.*

Thanks to [Martin Prikryl](https://stackoverflow.com/users/850848/martin-prikryl)

`auto_add_key` adds the key to knownhosts if the host key does not exist.


```python
    import pysftp

    with pysftp.Connection('hostname', username='me', password='secret', auto_add_key=True) as sftp:
        with sftp.cd('public'):             # temporarily chdir to public
            sftp.put('/my/local/filename')  # upload file to public/ on remote
            sftp.get('remote_file')         # get a remote file
```

Supports
--------

Tested on Python 2.7, 3.2, 3.3, 3.4
- currently no tests for `auto_add_key` 

.. Original Source:
* Project:  https://bitbucket.org/dundeemt/pysftp
* Download: https://pypi.python.org/pypi/pysftp
* Documentation: http://pysftp.rtfd.org/
