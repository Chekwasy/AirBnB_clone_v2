#!/usr/bin/python3

from fabric.api import env, run, put

env.hosts = ['34.239.207.21', '54.236.225.49']
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


def do_deploy(archive_path):
        """deploy the archive to your server
        """
        fd = archive_path.split("/")[1]
        try:
            put(archive_path, "/tmp/{}".format(fd))
            run("mkdir -p /data/web_static/releases/{}".format(fd))
            run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(fd, fd))
            run("rm /tmp/{}".format(fd))
            run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(fd, fd))
            run("rm -rf /data/web_static/releases/{}/web_static".format(fd))
            run("rm -rf /data/web_static/current")
            run("ln -sf /data/web_static/releases/{}/\
            /data/web_static/current".format(fd))
            print("Version successfully deployed!")
            return True
        except:
            print("Deployment failed.")
            return False
