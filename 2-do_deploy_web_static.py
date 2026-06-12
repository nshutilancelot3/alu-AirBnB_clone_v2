#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers."""
from fabric.api import env, put, run
import os

env.hosts = ['44.211.45.35', '44.211.161.173']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distribute an archive to the web servers and deploy it.

    Uploads the archive to /tmp/, extracts it to the releases directory,
    updates the symbolic link to point to the new release, and cleans up.
    Returns True if all operations succeed, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_filename = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_filename)[0]
        release_path = "/data/web_static/releases/{}/".format(archive_no_ext)

        put(archive_path, "/tmp/{}".format(archive_filename))
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))
        run("rm /tmp/{}".format(archive_filename))
        run("mv {}web_static/* {}".format(release_path, release_path))
        run("rm -rf {}web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        print("New version deployed!")
        return True

    except Exception:
        return False
