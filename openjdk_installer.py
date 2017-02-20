import subprocess
from logging import *


def openjdk_install():

    java_package = 'openjdk-8-jre'

    sys.stdout.write('Use defaults?: ')
    defaults = raw_input()

    if defaults != '' and defaults[0] != 'y':
        sys.stdout.write('Java Package Name: ')
        tmp_input = raw_input()
        if tmp_input != "":
            java_package = tmp_input

    try:
        d = subprocess.check_call(["apt-get", "update", "-y"])
        d = subprocess.check_call(["apt-get", "upgrade", "-y"])
        log("INFO", "updated and upgraded apt-get")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot update / upgrade apt-get")

    try:
        d = subprocess.check_call(["apt-get", "install", "-y", "apt-transport-https", "openjdk-8-jre-headless", "uuid-runtime", "pwgen"])
        log("INFO", "apt-transport, openjdk, uuid-runtime and pwgen dependencies installed")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install apt-transport, openjdk, uuid-runtime and pwgen dependencies")

    try:
        d = subprocess.check_call(["apt-get", "install", "-y", java_package])
        print "java 8 installed"
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install Java")