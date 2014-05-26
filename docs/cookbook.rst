Cook Book
=========

While in many ways, pysftp is just a thin wrapper over paramiko's SFTPClient,
there are a number of ways that we make it more productive and easier to
accomplish common, higher-level tasks.  The following snippets show where we
add value to this great module.

pysftp.Connection
-----------------
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

pysftp.Connection.get
---------------------
In addition to the normal paramiko call, you can optionally set the
``preserve_mtime`` parameter to ``True`` and the operation will make sure that
the modification times on the local copy match those on the server.

.. code-block:: python

    # ...
    sftp.get('myfile', preserve_mtime=True)

pysftp.Connection.get_d
-----------------------
This method is an abstraction above :meth:`.get` that allows you to copy all
the files in a remote directory to a local path.

pysftp.Connection.get_r
-----------------------

pysftp.Connection.put
---------------------
In addition to the normal paramiko call, you can optionally set the
``preserve_mtime`` parameter to ``True`` and the operation will make sure that
the modification times on the server copy match those on the local.

.. code-block:: python

    # ...
    sftp.put('myfile', preserve_mtime=True)

pysftp.Connection.put_d
-----------------------

pysftp.Connection.put_r
-----------------------

pysftp.Connection.cd
-----------------------

pysftp.Connection.cwd
-----------------------

pysftp.Connection.chmod
-----------------------

