Cook Book
=========

While in many ways, pysftp is just a thin wrapper over paramiko's SFTPClient,
there are a number of ways that we make it more productive and easier to
accomplish common, higher-level tasks.  The following snippets show where we
add value to this great module.  See the :doc:`pysftp` docs for a complete
listing.

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
    sftp.get_d('public', 'local-backup', preserve_mtime=True)

:meth:`pysftp.Connection.get_r`
-------------------------------
This pysftp method is an abstraction that recursively copies files *and*
directories from the remote to a local path.

.. code-block:: python

    # copy all files AND directories under public to a local path
    sftp.get_r('public', 'local-backup', preserve_mtime=True)

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

:meth:`pysftp.Connection.chmod`
-------------------------------
:meth:`.chmod` is a wrapper around paramiko's except for the fact it will
takes an integer representation of the octal mode.  No leading 0 or 0o
wanted.  We know it's suppose to be an octal, but who really remembers that?

This way it is just like a command line ``chmod 644 readme.txt``
::

    user group other
    rwx  rwx   rwx
    421  421   421

    user  - read/write = 4+2 = 6
    group - read       = 4   = 4
    other - read       = 4   = 4

.. code-block:: python

    sftp.chmod('readme.txt', 644)


:func:`pysftp.st_mode_to_int`
------------------------------
converts an octal mode result back to an integer representation.  The .st_mode
information returned in SFTPAttribute object .stat(*fname*).st_mode contains
extra things you probably don't care about, in a form that has been converted
from octal to int so you won't recognize it at first.  This function clips the
extra bits and hands you the file mode bits in a way you'll recognize.

.. code-block:: python

    >>> attr = sftp.stat('readme.txt')
    >>> attr.st_mode
    33188
    >>> pysftp.st_mode_to_int(attr.st_mode)
    644

:meth:`pysftp.Connection.chown`
-------------------------------
pysftp's method allows you to specify just, gid or the uid or both.  If either
gid or uid is None *(default)*, then pysftp does a stat to get the current ids
and uses that to fill in the missing parameter because the underlying paramiko
method requires that you explicitly set both.

**NOTE** uid and gid are integers and relative to each system.  Just because you
are uid 102 on your local system, a uid of 102 on the remote system most likely
won't be your login.  You will need to do some homework to make sure that you
are setting these values as you intended.

:meth:`pysftp.Connection.cwd`
-----------------------------
:meth:`.cwd` is a synonym for :meth:`.chdir`.  Its purpose is to make transposing
hand typed commands at an sftp command line into those used by pysftp, easier
to do.

.. code-block:: python

    ...
    sftp.cwd('public')  # is equivalent to sftp.chdir('public')

:attr:`pysftp.Connection.pwd`
-------------
Returns the current working directory.  It returns the result of
`.normalize('.')` but makes your code and intention easier to read. Paramiko
has a method, :meth:`.getcwd()`, that we expose, but that method returns
``None`` if :meth:`.chdir` has
not been called prior.

.. code-block:: python

    ...
    >>> sftp.pwd
    '/home/test'

:meth:`pysftp.Connection.listdir`
---------------------------------
The difference here, is that pysftp's version returns a sorted list instead of
paramiko's arbitrary order. Sorted by filename.

:meth:`pysftp.Connection.listdir_attr`
--------------------------------------
The difference here, is that pysftp's version returns a sorted list instead of
paramiko's arbitrary order. Sorted by filename.

:meth:`pysftp.Connection.makedirs`
----------------------------------
A common scenario where you need to create all directories in a path as
needed, setting their mode, if created. Takes a mode argument, just like
:meth:`.chmod`, that is an integer representation of the mode you want.

:meth:`pysftp.Connection.mkdir`
-------------------------------
Just like :meth:`.chmod`, the mode is an integer representation of the octal
number to use.  Just like the unix cmd, `chmod` you use 744 not 0744 or 0o744.

:meth:`pysftp.Connection.isdir`
-------------------------------
Does all the busy work of stat'ing and dealing with the stat module returning
a simple True/False.

:meth:`pysftp.Connection.isfile`
--------------------------------
Does all the busy work of stat'ing and dealing with the stat module returning
a simple True/False.

:meth:`pysftp.Connection.readlink`
----------------------------------
The underlying paramiko method can return either an absolute or a relative path.
pysftp forces this to always be an absolute path by laundering the result with
a `.normalize` before returning.

:meth:`pysftp.Connection.exists`
--------------------------------
Returns True if a remote entity exists

:meth:`pysftp.Connection.lexists`
----------------------------------
Like :meth:`.exists`, but returns True for a broken symbolic link

:meth:`pysftp.Connection.truncate`
----------------------------------
Like the underlying .truncate method, by pysftp returns the file's new size
after the operation.

:meth:`pysftp.Connection.walktree`
----------------------------------
Is a powerful method that can recursively (*default*) walk a **remote** directory
structure and calls a user-supplied callback functions for each file, directory
or unknown entity it encounters.  It is used in the get_x methods of pysftp
and can be used with great effect to do your own bidding.  Each callback is
supplied the pathname of the entity. (form: ``func(str)``)

:attr:`pysftp.Connection.sftp_client`
-------------------------------------
Don't like how we have over-ridden or modified a paramiko method? Use this
attribute to get at paramiko's original version.  Remember, our goal is to
augment not supplant paramiko.

:attr:`pysftp.path_advance`
----------------------------
generator to iterate over a file path

.. code-block:: python

    ...
    >>> list(sftp.path_advance('./pub/example/example01')
    ['./pub', './pub/example', './pub/example/example01']

:attr:`pysftp.path_retreat`
----------------------------
generator to iterate over a file path in reverse

.. code-block:: python

    ...
    >>> list(sftp.path_retreat('./pub/example/example01')
    ['./pub/example/example01', './pub/example', './pub']

:attr:`pysftp.reparent`
-----------------------
Pythons ``os.path.join('backup', '/home/test/pub')`` returns '/home/test/pub',
but if you want to copy a directory structure to a new path this won't do what
you want.  But, reparent will.

.. code-block:: python

    ...
    >>> reparent('backup', '/home/test/pub')
    'backup/./home/test/pub'

:attr:`pysftp.walktree`
-----------------------
Is similar to :meth:`pysftp.Connection.walktree` except that it walks a **local**
directory structure.  It has the same callback mechanism.

:attr:`pysftp.cd`
-----------------------
A with-context aware version of ``os.chdir`` for use on the **local** file
system.  The yin to :meth:`pysftp.Connection.cd` yang.

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

Paramiko also tries very hard to stay true to Python's ``os`` module, which
means sometimes, things are weird or a bit too low level.  We think paramiko's
goals are good and don't believe they should change. Those changes are for an
abstraction library like pysftp.
