#!/usr/bin/env python3
"""Fabfile to deploy HolbertonBnB to a web server.

Run `fab --list` to list all available commands.

Usage:
    `fab <script> --<option>=<value>`
Options:
    pack --folder=STR - Creates a tar archive.
    upload --archive=STR - Distributes a tar archive.
    pack-and-upload --folder=STR - Creates and distributes a tar archive.
    restart - Restarts the WSGI apps.
    deploy --folder=STR - All of the above for a given folder(s).
"""
import os.path
from datetime import datetime
from fabric import task
from invoke.exceptions import UnexpectedExit

hosts = ["ubuntu@3.216.240.188"]


@task(hosts=hosts)
def pack(connection, folder):
    """Create a tar archive of a given folder.

    Packs the folder in the format `versions/{folder}-{date}.tgz`.

    Args:
        folder (str): The name of the folder to pack.
    """
    dt = datetime.utcnow()
    file = f"versions/{folder}-{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}.tgz"

    if os.path.isdir("versions") is False:
        connection.local("mkdir -p versions")

    print(f"Packing {folder}... ")
    connection.local(f"tar -cvzf {file} {folder}")
    print("done.")
    return file


@task(hosts=hosts)
def upload(connection, archive):
    """Distributes an archive to a web server.

    Expects an archive in the format `versions/{folder}-{date}.tgz`.

    Args:
        archive (str): The name of the archive to distribute.
    """
    if os.path.isfile(archive) is False:
        return

    file = archive.split("/")[-1]
    folder = file.split("-")[0]

    print(f"Uploading {folder}... ")
    connection.put(archive, f"/tmp/{file}")
    connection.run(f"rm -rf /data/{folder}/")
    connection.run(f"mkdir -p /data/{folder}/")
    connection.run(f"tar -xzf /tmp/{file} -C /data/{folder}/")
    connection.run(f"rm /tmp/{file}")
    connection.run(f"mv /data/{folder}/{folder}/* /data/{folder}/")
    connection.run(f"rm -rf /data/{folder}/{folder}")
    print("done.")


@task(hosts=hosts)
def pack_and_upload(connection, folder):
    """Archives and distributes a folder to the server.

    Args:
        folder (str): The name of the folder to pack and upload.
    """
    archive = pack(connection, folder)
    upload(connection, archive)


@task(hosts=hosts)
def restart(connection):
    """Restarts the HolbertonBnB WSGI apps."""
    try:
        connection.run("pkill gunicorn")
    except UnexpectedExit:
        pass

    print("Restarting Gunicorn instances... ")
    gunicorn = "/home/ubuntu/.local/bin/gunicorn"
    connection.run(
        f"{gunicorn} --chdir /data/ --bind 0.0.0.0:5001 web_flask.hbnb:app --daemon"
    )
    connection.run(
        f"{gunicorn} --chdir /data/ --bind 0.0.0.0:5002 api.v1.app:app --daemon"
    )
    print("boom! All deployed!")


@task(hosts=hosts)
def deploy(connection, folder="all"):
    """Archives, distributes and runs the Gunicorn instance of a folder on the server.

    Args:
        folder (str): The name of the folder to pack and upload.
    """
    if folder == "all":
        [pack_and_upload(connection, f) for f in ["models", "api", "web_flask"]]
    else:
        pack_and_upload(connection, folder)
    restart(connection)
