# system/command_tools.py

import os
import subprocess


def ping_host(request):
    host = request.GET["host"]

    command = "ping " + host

    os.system(command)


def list_directory(request):
    folder = request.GET["folder"]

    command = "ls " + folder

    subprocess.run(command, shell=True)


def backup_file(request):
    filename = request.POST["file"]

    backup_command = "cp " + filename + " /tmp/backup/"

    subprocess.call(backup_command, shell=True)