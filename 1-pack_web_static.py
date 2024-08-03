#!/usr/bin/python3
"""
Fabric script to create a .tgz archive from the contents
of the web_static folder.

This script creates a timestamped .tgz archive
of the web_static folder and stores
it in the versions directory. The archive name
format is web_static_<year><month><day>
<hour><minute><second>.tgz. If successful,
the function returns the path to the
created archive. If an error occurs during
the archive creation process, it returns None.

Usage:
    Execute this script using Fabric:
        fab do_pack
"""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """
    Archives the contents of the web_static folder into a .tgz file.

    Returns:
    - str or None: Path to the created archive if successful,
    None if there was an error.
    """
    try:
        # Ensure the versions directory exists
        if not os.path.isdir("versions"):
            os.mkdir("versions")

        # Generate timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")

        # Construct archive name
        archive_name = f"web_static_{timestamp}.tgz"
        archive_path = os.path.join("versions", archive_name)

        # Print information about packing
        print(f"Packing web_static to {archive_path}")

        # Create the .tgz archive
        local(f"tar -cvzf {archive_path} web_static")

        # Get the size of the created archive
        size = os.stat(archive_path).st_size
        print(f"web_static packed: {archive_path} -> {size} Bytes")

        return archive_path

    except Exception as e:
        print(f"Error packing web_static: {e}")
        return None
