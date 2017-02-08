
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
"""

import subprocess
import sys

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
        d = subprocess.check_call(["apt-get", "install", javaPackage])
        print "java 8 installed"
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install Java")


def mongodb_install():
    mongoPackage = 'mongodb-server'

    try:
        d = subprocess.check_call(["apt-get", "install", mongoPackage])
        print "mongodb-server installed"
    except:
        log("ERROR", "Cannot install MongoDB")

def graylog_install():
    print "OK"

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

main()