
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

import hashlib

from logging import *
from openjdk_installer import  *
from elasticsearch_installer import *


def isInteger(value):
    try:
        int(value)
        return 0
    except ValueError:
        return 1


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
        d = subprocess.check_call(["apt-get", "update"])
        d = subprocess.check_call(["apt-get", "install", "graylog-server"])
        log("INFO", "graylog-server installed")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install graylog-server")


def graylog_configuration():

    config_location = "/etc/graylog/server/server.conf"
    configuration = None

    try:
        with open('server.conf') as conf_file:
            configuration = conf_file.readlines()
        log("INFO", "reading " + config_location)
    except IOError:
        log('ERROR', "Failed reading " + config_location)

    # sys.stdout.write('Enable Web Server? (y/n): ')
    web_enable = "true"  # assumed yes

    sys.stdout.write('Web Server IP: ')
    web_ip = raw_input()

    sys.stdout.write('admin password: ')
    password = raw_input()

    # sys.stdout.write('node is master? (y/n): ')
    is_master = "true"  # assumed yes

    pw_pepper = None

    log_retention = None

    while isInteger(log_retention) == 1:
        sys.stdout.write('log retention (in days): ')
        log_retention = raw_input()
        if isInteger(log_retention) == 1:
            log("WARNING", "Please try again, log retention must be given as a number.")

    try:
        d = subprocess.Popen(["pwgen", "-s", "96", "1"], stdout=subprocess.PIPE)
        pw_pepper, err = d.communicate()
    except subprocess.CalledProcessError:
        log('ERROR', "Creating password pepper failed.")

    try:
        pwd_hash = hashlib.sha256(password)

        web_enable_found = False

        for index, line in enumerate(configuration):
            if line.find("root_password_sha2 =") != -1:
                configuration[index] = "root_password_sha2 = " + pwd_hash.hexdigest()
            if line.find("password_secret = ") != -1:
                configuration[index] = "password_secret = " + pw_pepper
            if line.find("is_master = ") != -1:
                configuration[index] = "is_master = " + is_master
            if line.find("rest_listen_uri = ") != -1:
                configuration[index] = "rest_listen_uri = http://" + web_ip + ":9000/api/"
            if line.find("rest_transport_uri = ") != -1:
                configuration[index] = "rest_transport_uri = http://" + web_ip + ":9000/api/"
            if line.find("web_enable = ") != -1:
                configuration[index] = "web_enable = " + web_enable
                web_enable_found = True
            if line.find("web_listen_uri = ") != -1:
                configuration[index] = "web_listen_uri = http://" + web_ip + ":9000/"
            if line.find("elasticsearch_max_time_per_index = "):
                configuration[index] = "elasticsearch_max_time_per_index = 1d"
            if line.find("elasticsearch_max_number_of_indices = "):
                configuration[index] = "elasticsearch_max_number_of_indices = " + log_retention

        if web_enable_found == False:
            configuration.append("web_enable = " + web_enable)

        conf_file = open(config_location, 'w')
        conf_file.truncate()
        conf_file.writelines("".join(configuration))
    except:
        log('ERROR', "changing admin password failed.")




def main():

    # change ip, dns, gateway and hostname settings
    # deprecated for now.
    # configure_host()

    # install openjdk-x-jre-
    openjdk_install()

    # install mongodb-server
    mongodb_install()

    # install elasticsearch
    elasticsearch_install()

    # install graylog-server
    graylog_install()

    # make configuration changes
    graylog_configuration()

main()
