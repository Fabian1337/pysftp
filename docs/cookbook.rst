Cook Book
=========

While in many ways, pysftp is just a thin wrapper over paramiko's SFTPClient,
there are a number of ways that we make it more productive and easier to
accomplish common, higher-level tasks.  The following snippets show where we
add value to this great module.

:meth:`pysftp.Connection`
-------------------------
The Connection object is the base of pysftp.  It supports connections via
username and password.

.. code-block:: python

    import pysftp
    sftp = pysftp.Connection('hostname', username='me', password='secret')
    #
    # ... do sftp operations
    #
    sftp.close()    # close your connection to hostname

The Connection object is also context aware so you can use it with a ``with``
statement.

.. code-block:: python

    import pysftp
    with pysftp.Connection('hostname', username='me', password='secret') as sftp:
        #
        # ... do sftp operations
        #
    # connection closed automatically at the end of the with-block

Want to use an RSA or DSA key pair, that is simple too.

.. code-block:: python

    import pysftp
    with pysftp.Connection('hostname', private_key='/path/to/keyfile') as sftp:
        #
        # ... do sftp operations
        #

If you key is password protected, just add ``private_key_pass`` to the argument list.

How about a ``paramiko.AgentKey`` ? no problem, just set the private_key equal to it.

.. code-block:: python

    import pysftp
    with pysftp.Connection('hostname', private_key=my_agentkey) as sftp:
        #
        # ... do sftp operations
        #

The connection object also allows you to use an IP Address for the ``host`` and
you can set the ``port`` which defaults to 22, as well.

Here is a common scenario, you have your connection information stored in a
persistence mechanism, like `yamjam <http://yamjam.rtfd.org/>`_ and when you access
it, it is returned in dictionary form.  ``{'host':'myhost', username:'me', ...}``
Just send the dict into the connection object like so:

.. code-block:: python

    import pysftp
    cinfo = {'host':'hostname', 'username':'me', 'password':'secret', 'port':2222}
    with pysftp.Connection(**cinfo) as sftp:
        #
        # ... do sftp operations
        #

:meth:`pysftp.Connection.get`
-----------------------------
In addition to the normal paramiko call, you can optionally set the
``preserve_mtime`` parameter to ``True`` and the operation will make sure that
the modification times on the local copy match those on the server.

.. code-block:: python

    # ...
    sftp.get('myfile', preserve_mtime=True)

:meth:`pysftp.Connection.get_d`
-------------------------------
This pysftp method is an abstraction above :meth:`.get` that allows you to copy
all the files in a remote directory to a local path.

.. code-block:: python

    # copy all files under public to a local path, preserving modification time
    sftp.get_d('public', 'local-backup`, preserve_mtime=True)

:meth:`pysftp.Connection.get_r`
-------------------------------
This pysftp method is an abstraction that recursively copies files *and*
directories from the remote to a local path.

.. code-block:: python

    # copy all files AND directories under public to a local path
    sftp.get_r('public', 'local-backup`)

:meth:`pysftp.Connection.put`
-----------------------------
In addition to the normal paramiko call, you can optionally set the
``preserve_mtime`` parameter to ``True`` and the operation will make sure that
the modification times on the server copy match those on the local.

.. code-block:: python

    # copy myfile, to the current working directory on the server, preserving modification time
    sftp.put('myfile', preserve_mtime=True)

:meth:`pysftp.Connection.put_d`
-------------------------------
The opposite of :meth:`.get_d`, put_d allows you to copy the contents of a
local directory to a remote one via SFTP.

.. code-block:: python

    # copy files from images, to remote static/images directory, preserving modification time
    sftp.put_d('images', 'static/images' preserve_mtime=True)


:meth:`pysftp.Connection.put_r`
-------------------------------
This method copies all files *and* directories from a local path to a remote path.
It creates directories, and happily succeeds even if the target directories already exist.

.. code-block:: python

    # recursively copy files and directories from local static, to remote static,
    # preserving modification times on the files
    sftp.put_r('static', 'static' preserve_mtime=True)


:meth:`pysftp.Connection.cd`
----------------------------
This method is a with-context capable version of :meth:`.chdir`. Restoring the
original directory when the ``with`` statement goes out of scope. It can be
called with a remote directory to temporarily change to

.. code-block:: python

    with sftp.cd('static'):     # now in ./static
        sftp.chdir('here')      # now in ./static/here
        sftp.chdir('there')     # now in ./static/here/there
    # now back to the original current working directory

Or it can be called without a remote directory to just act as a bookmark you
want to return to later.

.. code-block:: python

    with sftp.cd():             # still in .
        sftp.chdir('static')    # now in ./static
        sftp.chdir('here')      # now in ./static/here
    # now back to the original current working directory

:meth:`pysftp.Connection.cwd`
-----------------------------
:meth:`.cwd` is a synonym for :meth:`.chdir`.  Its purpose is to make transposing
hand typed commands at an sftp command line into those used by pysftp, easier
to do.

.. code-block:: python

    sftp.cwd('public')  # is equivalent to sftp.chdir('public')

:meth:`pysftp.Connection.chmod`
-------------------------------

Remarks
-------
We think paramiko is a great python library and it is the backbone of pysftp.
The methods pysftp has created are abstractions that serve a programmer's
productivity by encapsulating many of the higher function use cases of
interacting with SFTP.  Instead of writing your own code to walk directories
and call get and put, dealing with not only paramiko but Python's own ``os``
and ``stat`` modules and writing tests *(many code snippets on the net are
incomplete and don't account for edge cases)* pysftp supplies a complete
library for dealing with all 3.  Leaving you to focus on your primary task.
