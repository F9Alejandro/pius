'''A set of path functions and variables for the PIUS suite.'''
from __future__ import print_function

import os
import sys
import stat
from libpius.constants import BIN_PATHs, LINUX_TEMPDIR
from os.path import abspath
import fnmatch

LINUX_TEMPDIR = '/tmp/'
BIN_PATHS = '/usr/bin;/usr/sbin/;/bin;/sbin;/usr/local/bin;/usr/local/sbin'
'''This is grabbed right from the python repo under lib/shutil.py'''

def which(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.
    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.
    """
    # Check that a given file can be accessed with the correct mode.
    # Additionally check that `file` is not a directory, as on Windows
    # directories pass the os.access check.
    def _access_check(fn, mode):
        return (os.path.exists(fn) and os.access(fn, mode)
                and not os.path.isdir(fn))

    # If we're given a path with a directory part, look it up directly rather
    # than referring to PATH directories. This includes checking relative to the
    # current directory, e.g. ./script
    if os.path.dirname(cmd):
        if _access_check(cmd, mode):
            return cmd
        return None

    if path is None:
        path = os.environ.get("PATH", os.defpath)
    if not path:
        return None
    path = path.split(os.pathsep)

    if sys.platform == "win32":
        # The current directory takes precedence on Windows.
        if not os.curdir in path:
            path.insert(0, os.curdir)

        # PATHEXT is necessary to check on Windows.
        pathext = os.environ.get("PATHEXT", "").split(os.pathsep)
        # See if the given file matches any of the expected path extensions.
        # This will allow us to short circuit when given "python.exe".
        # If it does match, only test that one, otherwise we have to try
        # others.
        if any(cmd.lower().endswith(ext.lower()) for ext in pathext):
            files = [cmd]
        else:
            files = [cmd + ext for ext in pathext]
    else:
        # On other platforms you don't have things like PATHEXT to tell you
        # what file suffixes are executable, so just pass on cmd as-is.
        files = [cmd]

    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if not normdir in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None

def gpg_path():
    if sys.platform = "win32":
        gpg = which('gpg2')
    elif:
        gpg = which('gpg2',path=BIN_PATHS)
    if gpg == "":
        print("GPG2 could not be found! Do you have the correct permissions?")
        sys.exit(1)
    else:
        return gpg

def get_home():
    if sys.platform == "win32":
        return os.environ.get('APPDATA')
    else:
        return os.environ.get('HOME')

def get_gpghome(usrhome):
    if sys.platform == "win32":
        return os.environ.get('GNUPGHOME', os.path.join(usrhome, 'roaming\/gnupg'))
    else:
        return os.environ.get('GNUPGHOME', os.path.join(usrhome, '.gnupg'))

def get_piushome(usrhome):
    if sys.platform == "win32":
        return os.path.join(usrhome, 'roaming\/pius')
    else:
        return os.path.join(usrhome, '.pius')

def get_tmpdir(dir):
    if sys.platform == "win32":
        tempdir = os.environ.get('TEMP')
        return os.path.join(tempdir, dir)
    elif sys.platform == "darwin":
        if os.environ.get('USER') == "root":
            tempdir = '/private/tmp/'
        else:
            tempdir = os.environ.get('TMPDIR')
        return os.path.join(tempdir, dir)
    else:
        if os.environ.get('USER') == "root":
            tempdir = os.path.join('/tmp/', dir)
        elif os.environ.get('XDG_RUNTIME_DIR') != "":
            tempdir = os.path.join(os.environ.get('XDG_RUNTIME_DIR'), dir)
        elif os.environ.get('TMPDIR') != "":
            tempdir = os.path.join(os.environ.get('TMPDIR'), dir)
        else:
            tempdir = os.path.join(LINUX_TEMP, dir)
        return tempdir 

# END Stupid python optparse hack.
