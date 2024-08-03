#!/usr/bin/python3
"""
Fabfile to delete out-of-date archives.

This script defines a Fabric task to delete out-of-date
archives both locally and
on remote servers defined in env.hosts.

Functions:
- do_clean(number=0): Deletes out-of-date archives based on
the specified number.
  Args:
  - number (int): Number of most recent archives to keep.
  Default is 0, which keeps
    only the most recent archive.

Notes:
- Local Cleanup: Removes archives from the 'versions' directory.
- Remote Cleanup: Removes releases from '/data/web_static/releases'
on remote servers.
"""
import os
from fabric.api import *

env.hosts = ["100.26.221.187", "54.172.185.100"]


def do_clean(number=0):
    """
    Delete out-of-date archives from local and remote directories.

    Args:
    - number (int): Number of archives to keep. If 0 or 1,
    keeps only the most recent archive.
      If 2, keeps the two most recent archives, and so on.

    Notes:
    - Local Cleanup: Removes out-of-date archives
    from the 'versions' directory.
    - Remote Cleanup: Removes out-of-date releases
    from '/data/web_static/releases'.
    """
    number = 1 if int(number) == 0 else int(number)

    # Local cleanup
    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Remote cleanup
    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
