#!/usr/bin/python3
"""
Fabfile to create and distribute an archive to a web server.

This script defines functions to create a tar gzipped
archive of the web_static directory
and distribute it to specified remote web servers.
It uses Fabric's API for file operations
and remote execution.

Functions:
- do_pack(): Creates a timestamped tar.gz
archive of the web_static directory locally.
  Returns the path to the archive if successful,
  or None if creation fails.

- do_deploy(archive_path): Distributes an
archive to the remote web servers.
  Args:
  - archive_path (str): Path to the archive to distribute.
  Returns:
  - True if deployment succeeds, False otherwise.

- deploy(): Combines do_pack and do_deploy functions to
automate archive creation and deployment.
  Returns:
  - True if both packing and deployment succeed, False otherwise.

Requirements:
- Fabric must be installed (`pip install fabric`).
- Ensure SSH access and permissions are properly configured for remote servers.
- Run using Fabric's `fab` command to execute functions.
"""

import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["52.91.121.146", "3.85.136.181"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
