"""A friendly Python SFTP interface."""

import os
import socket
from stat import S_IMODE, S_ISDIR, S_ISREG
import tempfile
import paramiko
from paramiko import SSHException   # make available
from paramiko import AuthenticationException   # make available
from paramiko import AgentKey

__version__ = "0.2.6"


def st_mode_to_int(val):
    '''SFTAttributes st_mode returns an stat type that shows more than what
    can be set.  Trim off those bits and convert to an int representation.
    if you want an object that was `chmod 711` to return a value of 711, use
    this function

    :param int val: the value of an st_mode attr returned by SFTPAttributes

    :returns int: integer representation of octal mode

    '''
    return int(str(oct(S_IMODE(val))))


class ConnectionException(Exception):
    """Exception raised for connection problems

    Attributes:
        message  -- explanation of the error
    """

    def __init__(self, host, port):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, host, port)
        self.message = 'Could not connect to host:port.  %s:%s'

class CredentialException(Exception):
    """Exception raised for credential problems

    Attributes:
        message  -- explanation of the error
    """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.message = message


class Connection(object):
    """Connects and logs into the specified hostname.
    Arguments that are not given are guessed from the environment.

    :param str host: The Hostname or IP of the remote machine.
    :param str username: Your username at the remote machine.
    :param private_key: path to private key file(str) or paramiko.AgentKey
    :param str password: Your password at the remote machine.
    :param int port: The SSH port of the remote machine.(default: 22)
    :param str private_key_pass: password to use, if private_key is encrypted.
    :param list ciphers: List of ciphers to use in order.
    :param bool|str log:
        log connection/handshake details? (default=False) if set to True,
        pysftp creates a temporary file and logs to that.  If set to a valid
        path and filename, pysftp logs to that.  The name of the logfile can
        be found at  ``.logfile``
    :returns: a connection to the requested host
    :raises:
        ConnectionException, CredentialException, SSHException,
        AuthenticationException, PasswordRequiredException

    """

    def __init__(self,
                 host,
                 username=None,
                 private_key=None,
                 password=None,
                 port=22,
                 private_key_pass=None,
                 ciphers=None,
                 log=False,
                ):
        self._sftp_live = False
        self._sftp = None
        if not username:
            username = os.environ['LOGNAME']


        self._logfile = log
        if log:
            if isinstance(log, bool):
                # Log to a temporary file.
                fhnd, self._logfile = tempfile.mkstemp('.txt', 'ssh-')
                os.close(fhnd)  # don't want os file descriptors open
            paramiko.util.log_to_file(self._logfile)

        # Begin the SSH transport.
        self._transport_live = False
        try:
            self._transport = paramiko.Transport((host, port))
            # Set security ciphers if set
            if ciphers is not None:
                self._transport.get_security_options().ciphers = ciphers
            self._transport_live = True
        except (AttributeError, socket.gaierror):
            # couldn't connect
            raise ConnectionException(host, port)

        # Authenticate the transport. prefer password if given
        if password is not None:
            # Using Password.
            self._transport.connect(username=username, password=password)
        else:
            # Use Private Key.
            if not private_key:
                # Try to use default key.
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key = '~/.ssh/id_rsa'
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key = '~/.ssh/id_dsa'
                else:
                    raise CredentialException("You have not specified a "\
                                              "password or key.")
            if not isinstance(private_key, AgentKey):
                private_key_file = os.path.expanduser(private_key)
                try:  #try rsa
                    rsakey = paramiko.RSAKey
                    prv_key = rsakey.from_private_key_file(private_key_file,
                                                           private_key_pass)
                except paramiko.SSHException:   #if it fails, try dss
                    dsskey = paramiko.DSSKey
                    prv_key = dsskey.from_private_key_file(private_key_file,
                                                           private_key_pass)
            else:
                # use the paramiko agent key
                prv_key = private_key
            self._transport.connect(username=username, pkey=prv_key)

    def _sftp_connect(self):
        """Establish the SFTP connection."""
        if not self._sftp_live:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp_live = True

    def get(self, remotepath, localpath=None, callback=None,
            preserve_mtime=False):
        """Copies a file between the remote host and the local host.

        :param str remotepath: the remote path and filename, source
        :param str localpath:
            the local path and filename to copy, destination. If not specified,
            file is copied to local cwd
        :param callable callback:
            optional callback function (form: ``func(int, int)``) that accepts
            the bytes transferred so far and the total bytes to be transferred.
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            local file match the time on the remote. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns: nothing

        :raises: IOError

        """
        if not localpath:
            localpath = os.path.split(remotepath)[1]

        self._sftp_connect()
        if preserve_mtime:
            sftpattrs = self._sftp.stat(remotepath)

        self._sftp.get(remotepath, localpath, callback=callback)
        if preserve_mtime:
            os.utime(localpath, (sftpattrs.st_atime, sftpattrs.st_mtime))

    def getfo(self, remotepath, flo, callback=None):
        """Copy a remote file (remotepath) to a file-like object, flo.

        :param str remotepath: the remote path and filename, source
        :param flo: open file like object to write, destination.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred.

        :returns int: the number of bytes written to the opened file object

        :raises: Any exception raised by operations will be passed through.

        """
        self._sftp_connect()
        return self._sftp.getfo(remotepath, flo, callback=callback)

    def put(self, localpath, remotepath=None, callback=None, confirm=True,
            preserve_mtime=False):
        """Copies a file between the local host and the remote host.

        :param str localpath: the local path and filename
        :param str remotepath:
            the remote path, else the remote cwd() and filename is used.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred..
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size
        :param bool preserve_mtime:
            *Default: False* - make the modification time(st_mtime) on the
            remote file match the time on the local. (st_atime can differ
            because stat'ing the localfile can/does update it's st_atime)

        :returns:
            SFTPAttributes object containing attributes about the given file

        :raises: IOError, OSError

        """
        if not remotepath:
            remotepath = os.path.split(localpath)[1]
        self._sftp_connect()

        if preserve_mtime:
            local_stat = os.stat(localpath)
            times = (local_stat.st_atime, local_stat.st_mtime)

        sftpattrs = self._sftp.put(localpath, remotepath, callback=callback,
                                   confirm=confirm)
        if preserve_mtime:
            self._sftp.utime(remotepath, times)
            sftpattrs = self._sftp.stat(remotepath)

        return sftpattrs

    def putfo(self, flo, remotepath=None, file_size=0, callback=None,
              confirm=True):

        """Copies the contents of a file like object to remotepath.

        :param flo: a file-like object that supports .read()
        :param str remotepath: the remote path.
        :param int file_size:
            the size of flo, if not given the second param passed to the
            callback function will always be 0.
        :param callable callback:
            optional callback function (form: ``func(int, int``)) that accepts
            the bytes transferred so far and the total bytes to be transferred..
        :param bool confirm:
            whether to do a stat() on the file afterwards to confirm the file
            size

        :returns:
            SFTPAttributes object containing attributes about the given file

        :raises: TypeError if remotepath not specified, any underlying error

        """
        self._sftp_connect()
        return self._sftp.putfo(flo, remotepath, file_size=file_size,
                                callback=callback, confirm=confirm)

    def execute(self, command):
        """Execute the given commands on a remote machine.  The command is
        executed without regard to the remote cwd.

        :param str command: the command to execute.

        :returns: results

        :raises: Any exception raised by command will be passed through.

        """
        channel = self._transport.open_session()
        channel.exec_command(command)
        output = channel.makefile('rb', -1).readlines()
        if output:
            return output
        else:
            return channel.makefile_stderr('rb', -1).readlines()

    def chdir(self, remotepath):
        """change the current working directory on the remote

        :param str remotepath: the remote path to change to

        :returns: nothing

        :raises: IOError

        """
        self._sftp_connect()
        self._sftp.chdir(remotepath)

    def getcwd(self):
        """return the current working directory on the remote

        :returns: a string representing the current remote path

        """
        self._sftp_connect()
        return self._sftp.getcwd()

    def listdir(self, remotepath='.'):
        """return a list of files/directories for the given remote path

        :param str remotepath: path to list on the server

        :returns: a list of entries

        """
        self._sftp_connect()
        return self._sftp.listdir(remotepath)

    def mkdir(self, remotepath, mode=777):
        """Create a directory named remotepath with mode. On some systems,
        mode is ignored. Where it is used, the current umask value is first
        masked out.

        :param str remotepath: directory to create`
        :param int mode:
            int representation of octal mode for directory, default 777

        :returns: nothing

        """
        self._sftp_connect()
        self._sftp.mkdir(remotepath, mode=int(str(mode), 8))

    def isdir(self, remotepath):
        """return true if remotepath is a directory

        :param str remotepath: the path to test

        :returns bool:

        """
        self._sftp_connect()
        try:
            result = S_ISDIR(self._sftp.stat(remotepath).st_mode)
        except IOError:     # no such file
            result = False
        return result

    def isfile(self, remotepath):
        """return true if remotepath is a file

        :param str remotepath: the path to test

        :returns bool:

        """
        self._sftp_connect()
        try:
            result = S_ISREG(self._sftp.stat(remotepath).st_mode)
        except IOError:     # no such file
            result = False
        return result

    def makedirs(self, remotedir, mode=777):
        """create all directories in remotedir as needed, setting their mode
        to mode, if created.

        If remotedir already exists, silently complete. If a regular file is
        in the way, raise an exception.

        :param str remotedir: the direcotry structure to create
        :param int mode:
            int representation of octal mode for directory, default 777

        :returns: None

        :raises: OSError

        """
        self._sftp_connect()
        if self.isdir(remotedir):
            pass

        elif self.isfile(remotedir):
            raise OSError("a file with the same name as the remotedir, " \
                          "'%s', already exists." % remotedir)
        else:

            head, tail = os.path.split(remotedir)
            print remotedir, head, tail
            if head and not self.isdir(head):
                self.makedirs(head, mode)

            if tail:
                self.mkdir(remotedir, mode=mode)

    def remove(self, remotefile):
        """remove the file @ remotefile, remotefile may include a path, if no
        path, then cwd is used.  This method only works on files

        :param str remotefile: the remote file to delete

        :returns: nothing

        :raises: IOError

        """
        self._sftp_connect()
        self._sftp.remove(remotefile)

    def rmdir(self, remotepath):
        """remove remote directory

        :param str remotepath: the remote directory to remove

        :returns: nothing

        """
        self._sftp_connect()
        self._sftp.rmdir(remotepath)

    def rename(self, remote_src, remote_dest):
        """rename a file or directory on the remote host.

        :param str remote_src: the remote file/directory to rename

        :param str remote_dest: the remote file/directory to put it

        :returns: nothing

        :raises: IOError

        """
        self._sftp_connect()
        self._sftp.rename(remote_src, remote_dest)

    def stat(self, remotepath):
        """return information about file/directory for the given remote path

        :param str remotepath: path to stat

        :returns: SFTPAttributes object

        """
        self._sftp_connect()
        return self._sftp.stat(remotepath)

    def lstat(self, remotepath):
        """return information about file/directory for the given remote path,
        without following symbolic links. Otherwise, the same as .stat()

        :param str remotepath: path to stat

        :returns: SFTPAttributes object

        """
        self._sftp_connect()
        return self._sftp.lstat(remotepath)

    def close(self):
        """Closes the connection and cleans up."""
        # Close SFTP Connection.
        if self._sftp_live:
            self._sftp.close()
            self._sftp_live = False
        # Close the SSH Transport.
        if self._transport_live:
            self._transport.close()
            self._transport_live = False

    def open(self, remote_file, mode='r', bufsize=-1):
        """Open a file on the remote server.

        See http://paramiko-docs.readthedocs.org/en/latest/api/sftp.html?highlight=open#paramiko.sftp_client.SFTPClient.open for details.

        :param str remote_file: name of the file to open.
        :param str mode:
            mode (Python-style) to open file (always assumed binary)
        :param int bufsize: desired buffering (-1 = default buffer size)

        :returns: an SFTPFile object representing the open file

        :raises: IOError - if the file could not be opened.

        """
        self._sftp_connect()
        return self._sftp.open(remote_file, mode=mode, bufsize=bufsize)

    def exists(self, remotepath):
        """Test whether a remotepath exists.

        :param str remotepath: the remote path to verify

        :returns bool: True if remotepath exists, else False

        """
        self._sftp_connect()
        try:
            self._sftp.stat(remotepath)
        except IOError:
            return False
        return True

    def lexists(self, remotepath):
        """Test whether a remotepath exists.  Returns True for broken symbolic
        links

        :param str remotepath: the remote path to verify

        :returns bool: True if lexists, else False

        """
        self._sftp_connect()
        try:
            self._sftp.lstat(remotepath)
        except IOError:
            return False
        return True

    def symlink(self, remote_src, remote_dest):
        '''create a symlink for a remote file on the server

        :param str remote_src: path of original file
        :param str remote_dest: path of the created symlink

        :returns: None

        :raises:
            any underlying error, IOError if something already exists at
            remote_dest

        '''
        self._sftp_connect()
        self._sftp.symlink(remote_src, remote_dest)

    @property
    def active_ciphers(self):
        """Get tuple of currently used local and remote ciphers.

        :returns:
            a tuple of currently used ciphers (local_cipher, remote_cipher)

        """
        return self._transport.local_cipher, self._transport.remote_cipher

    @property
    def security_options(self):
        """return the available security options recognized by paramiko.

        :returns SecurityOptions:
            a simple object security preferences of an
            ssh transport. These are tuples of acceptable ciphers, digests,
            key types, and key exchange algorithms, listed in order of
            preference.

        """

        return self._transport.get_security_options()

    @property
    def logfile(self):
        '''return the name of the file used for logging or False it not logging

        :returns: logfile(str) or False(bool)

        '''
        return self._logfile

    def __del__(self):
        """Attempt to clean up if not explicitly closed."""
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, etype, value, traceback):
        self.close()

def path_advance(thepath, sep=os.sep):
    '''generator to iterate over a file path forwards

    :param str thepath: the path to navigate forwards
    :param str sep: the path separator to use, defaults to ``os.sep``

    :returns generator: of strings

    '''
    # handle a direct path
    pre = ''
    if thepath[0] == sep:
        pre = sep
    curpath = ''
    parts = thepath.split(sep)
    if pre:
        if parts[0]:
            parts[0] = pre + parts[0]
        else:
            parts[1] = pre + parts[1]
    for part in parts:
        curpath = os.path.join(curpath, part)
        if curpath:
            yield curpath

def path_retreat(thepath, sep=os.sep):
    '''generator to iterate over a file path in reverse

    :param str thepath: the path to retreat over
    :param str sep: the path separator to use, default to ``os.sep``

    :returns generator: of strings

    '''
    pre = ''
    if thepath[0] == sep:
        pre = sep
    parts = thepath.split(sep)
    while parts:
        if os.path.join(*parts):
            yield '%s%s' % (pre, os.path.join(*parts))
        parts = parts[:-1]
