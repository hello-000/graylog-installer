import subprocess
from logging import *


def openjdk_install():

    javaPackage = 'openjdk-8-jre'

    sys.stdout.write('Use defaults?: ')
    defaults = raw_input()

    if defaults != '' and defaults[0] != 'y':
        sys.stdout.write('Java Package Name: ')
        javaPackage = raw_input()

    try:
        d = subprocess.check_call(["apt-get", "update", "&&", "apt-get", "upgrade"])
        log("INFO", "updated and upgraded apt-get")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot update / upgrade apt-get")

    try:
        d = subprocess.check_call(["apt-get", "install", "apt-transport-https", "openjdk-8-jre-headless", "uuid-runtime", "pwgen"])
        log("INFO", "apt-transport, openjdk, uuid-runtime and pwgen dependencies installed")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install apt-transport, openjdk, uuid-runtime and pwgen dependencies")

    try:
        d = subprocess.check_call(["apt-get", "install", javaPackage])
        print "java 8 installed"
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install Java")