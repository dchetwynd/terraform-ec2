#!/usr/bin/python
import sys
import os
from subprocess import Popen

KEY_PAIR_NAME = "key_pair"


def _delete_file(name):
    if os.path.exists(name):
        os.remove(name)


def _delete_key_pair():
    _delete_file(KEY_PAIR_NAME)
    _delete_file("%s.pub" % KEY_PAIR_NAME)


def _run_command(command):
    process = Popen(command, shell=True)
    process.communicate()

    if process.returncode != 0:
        sys.exit()


def _get_public_key_contents():
    with open("%s.pub" % KEY_PAIR_NAME, "r") as public_key_file:
        return public_key_file.read().strip()


def _create_ssh_key_pair():
    _delete_key_pair()
    _run_command("ssh-keygen -f %s -t rsa -b 2048 -m 'PEM' -N '' -C ''" % KEY_PAIR_NAME)
    _run_command("chmod 400 %s" % KEY_PAIR_NAME)

    return _get_public_key_contents()


if __name__ == '__main__':
    public_key_contents = _create_ssh_key_pair()

    _run_command("terraform init")
    _run_command("terraform apply -var='public_key=%s'" % public_key_contents)