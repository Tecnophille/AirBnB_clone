# HolbertonBnB - Automatic Deployment Scripts :rocket:

Fabric and Puppet scripts for automatically, remotely deploying HolbertonBnB.

## Dependencies :couple:

| Tool/Library | Version |
| ------------ | ------- |
| Python       | ^3.7.3  |
| gunicorn     | ^19.9.0 |
| Fabric       | ^2.4.0  |
| Puppet       | ^5.4.0  |

## Usage :running:

* [setup_server.pp](../setup_server.pp): Puppet manifest that configures a web server for deployment of HolbertonBnB.
  * Usage: `sudo puppet apply setup_server.pp` (note that `sudo` privileges are required).
  * Ensures installation of Nginx, copies in an Nginx configuration file, and runs the service.
  * Creates the directory `/data` to store the application, set the proper permissions.

* [fabfile.py](../fabfile.py): Fabric fabfile to deploy HolbertonBnB to a web server.
  * Run `fab --list` to list all available commands.
  * Usage: `fab <script> --<option>=<value>`
  * Options:
    * `pack --folder=STR`: Creates a tar archive.
    * `upload --archive=STR`: Distributes a tar archive.
    * `pack-and-upload --folder=STR`: Creates and distributes a tar archive.
    * `restart`: Restarts the WSGI apps.
    * `deploy --folder=STR`: All of the above for a given folder(s).

## Author :black_nib:

* __Brennan D Baraban__ - <[bdbaraban](https://github.com/bdbaraban)>
