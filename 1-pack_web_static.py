#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the web_static folder."""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generate a tgz archive from the contents of the web_static folder.

    Returns the archive path if successfully created, otherwise None.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)

    local("mkdir -p versions")
    print("Packing web_static to {}".format(archive_path))

    result = local("tar -cvzf {} web_static".format(archive_path), capture=False)

    if result.failed:
        return None

    size = os.path.getsize(archive_path)
    print("web_static packed: {} -> {}Bytes".format(archive_path, size))

    return archive_path
