
"""
# This python script will install:
# 	openjdk-x-jre (java 8 or above)
# 	mongodb-server
# 	graylog-server
#	graylog-web (included in above package)
#
# A separate script will be used for installing elasticsearch,
# as it is recommended to keep these two instances separate.

# For further documentation on the installation of Graylog,
# please refer to the official documentation:
#   http://docs.graylog.org/en/2.1/pages/installation/os/ubuntu.html
#
# Please be aware, that this script is written for Ubuntu 16.04
# should it be installed on an Ubuntu 14.04, there are certain
# changes that need to be made, before running the script, as there
# is no native support for java-8.
"""

import subprocess
import sys
import hashlib

from printing import pcolors

def log(severity, msg):
    print "[*][" + severity + "] - " + msg
    if severity == 'ERROR':
        "[*][" + severity + "] - " + "Exiting script execution"
        sys.exit(1)

# Deprecated until further notice, fuck this ipconfig stuff.
def configure_host():

    # get variables for configuration

    sys.stdout.write('hostname: ')
    hostname = raw_input()

    sys.stdout.write('network-interface: ')
    interface = raw_input()

    sys.stdout.write('ip-address: ')
    ip_address = raw_input()

    sys.stdout.write('netmask: ')
    netmask = raw_input()

    sys.stdout.write('default-gateway: ')
    gateway = raw_input()

    sys.stdout.write('dns-server: ')
    nameserver = raw_input()

    try:
        hostname_file = open('/etc/hostname', 'w')
        hostname_file.truncate()
        hostname_file.write(hostname)

        log("INFO", "Hostname changed to " + hostname)
    except:
        log("ERROR", "Cannot change hostname")


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


def mongodb_install():
    mongoPackage = 'mongodb-server'

    try:
        d = subprocess.check_call(["apt-get", "install", mongoPackage])
        log("INFO", "mongodb-server installed")
    except:
        log("ERROR", "Cannot install MongoDB")

def graylog_install():
    print "OK"
    try:
        d = subprocess.check_call(["wget", "https://packages.graylog2.org/repo/packages/graylog-2.1-repository_latest.deb"])
        log("INFO", "retrieved graylog-2.1-repository_latest.deb from repository")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot retrieve graylog-2.1-repository_latest.deb from repository")

    try:
        d = subprocess.check_call(["dpkg", "-i", "graylog-2.1-repository_latest.deb"])
        log("INFO", "depackaged graylog-2.1-repository_latest.deb")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot depackage graylog-2.1-repository_latest.deb")

    try:
        d = subprocess.check_call(["apt-get", "update", "&&", "apt-get", "install", "graylog-server"])
        log("INFO", "graylog-server installed")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install graylog-server")



def graylog_configuration():

    configuration = None

    try:
        with open('server.conf') as file:
            configuration = file.readlines()
        log("INFO", "reading /etc/graylog/server/server.conf")
    except subprocess.CalledProcessError:
        log('ERROR', "Failed reading /etc/graylog/server/server.conf")

    sys.stdout.write('admin password: ')
    password = raw_input()

    try:

        pwd_hash = hashlib.sha256(password)

        for index, line in enumerate(configuration):
            if line.find("root_password_sha2 =") != -1:
                configuration[index] = "root_password_sha2 = " + pwd_hash.hexdigest()

        file = open('server.conf', 'w')
        file.truncate()
        file.writelines("".join(configuration))
    except subprocess.CalledProcessError:
        log('ERROR', "changing admin password failed.")

    try:
        d = subprocess.Popen(["pwgen", "-s", "96", "1"], stdout=subprocess.PIPE)
        out, err = d.communicate()
        print out
    except subprocess.CalledProcessError:
        log('ERROR', "Creating password pepper failed.")

def main():

    # change ip, dns, gateway and hostname settings
    # deprecated for now.
    # configure_host()

    # install openjdk-x-jre-
    # openjdk_install()

    # install mongodb-server
    # mongodb_install()

    # install graylog-server
    # graylog_install()

    # make configuration changes
    graylog_configuration()

main()
