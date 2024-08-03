#!/usr/bin/python3
"""
Fabric script to distribute an archive to remote web servers and deploy it.

This script connects to remote servers
defined in env.hosts and deploys a specified
archive to update the web application's static content.
It performs the following steps:
1. Uploads the archive to the /tmp/ directory on each server.
2. Uncompresses the archive to
/data/web_static/releases/<archive_filename_without_extension>/.
3. Deletes the uploaded archive from the server.
4. Updates the symbolic link /data/web_static/current
to point to the deployed version.

Requirements:
- Fabric must be installed (pip install fabric).
- Ensure SSH access and appropriate permissions are set on the remote servers.

Usage:
- Run this script using Fabric:
    fab -f <script_name.py> do_deploy:/path/to/your/archive.tgz
"""

from datetime import datetime
from fabric.api import env, put, run
import os

# Define remote hosts and user
env.hosts = ["100.26.221.187", "54.172.185.100"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.

    Args:
    - archive_path (str): Local path to the archive to deploy.

    Returns:
    - bool: True if deployment was successful, False otherwise.
    """
    if os.path.exists(archive_path):
        try:
            archive_filename = os.path.basename(archive_path)
            archive_name = os.path.splitext(archive_filename)[0]
            remote_path = f"/data/web_static/releases/{archive_name}"

            put(archive_path, "/tmp/")

            run(f"sudo mkdir -p {remote_path}")

            run(f"sudo tar -xzf /tmp/{archive_filename} -C {remote_path}/")

            run(f"sudo rm /tmp/{archive_filename}")

            # Move contents to proper location
            run(f"sudo mv {remote_path}/web_static/* {remote_path}/")

            # Remove empty web_static directory
            run(f"sudo rm -rf {remote_path}/web_static")

            # Update symbolic link
            run("sudo rm -rf /data/web_static/current")
            run(f"sudo ln -s {remote_path} /data/web_static/current")

            print("New version deployed successfully!")
            return True

        except Exception as e:
            print(f"Error deploying archive: {e}")
            return False

    else:
        print(f"Local archive '{archive_path}' not found.")
        return False
