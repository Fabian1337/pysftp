pysftp
======

.. automodule:: pysftp
   :members:



SFTPAttributes
--------------
  see http://paramiko-docs.readthedocs.org/en/latest/api/sftp.html?highlight=sftpattributes#paramiko.sftp_attr.SFTPAttributes for details

SFTPFile
--------
  see http://paramiko-docs.readthedocs.org/en/latest/api/sftp.html?highlight=paramiko.sftp_file.sftpfile#paramiko.sftp_file.SFTPFile for details


Callbacks
----------
callback function (form: ``func(int, int``)) where the first int is the bytes
transferred so far and the second int is the total bytes to be transferred.

**Note**: On a ``.putfo``, if you don't set the ``file_size`` parameter, it will always be
passed a zero, the default ``file_size`` value.

SecurityOptions
---------------
a simple object returned with available Security Options

see http://paramiko-docs.readthedocs.org/en/latest/api/transport.html?highlight=ciphers#paramiko.transport.SecurityOptions for details