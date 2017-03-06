
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
#   http://docs.graylog.org/en/2.2/pages/installation/os/ubuntu.html
#
# Please be aware, that this script is written for Ubuntu 16.04
# should it be installed on an Ubuntu 14.04, there are certain
# changes that need to be made, before running the script, as there
# is no native support for java-8.
"""

import hashlib

from logging import *
from openjdk_installer import *
from elasticsearch_installer import *
from elasticsearch_configuration import *


def isInteger(value):
    try:
        int(value)
        return 0
    except ValueError:
        return 1
    except TypeError:
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
        d = subprocess.check_call(["apt-get", "install", "-y", mongoPackage])
        log("INFO", "mongodb-server installed")
    except:
        log("ERROR", "Cannot install MongoDB")


def graylog_install():
    print "OK"
    try:
        d = subprocess.check_call(["wget", "https://packages.graylog2.org/repo/packages/graylog-2.2-repository_latest.deb"])
        log("INFO", "retrieved graylog-2.2-repository_latest.deb from repository")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot retrieve graylog-2.2-repository_latest.deb from repository")

    try:
        d = subprocess.check_call(["dpkg", "-i", "graylog-2.2-repository_latest.deb"])
        log("INFO", "depackaged graylog-2.2-repository_latest.deb")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot depackage graylog-2.2-repository_latest.deb")

    try:
        d = subprocess.check_call(["apt-get", "update", "-y"])
        d = subprocess.check_call(["apt-get", "install", "-y", "graylog-server"])
        log("INFO", "graylog-server installed")
    except subprocess.CalledProcessError:
        log('ERROR', "Cannot install graylog-server")


def graylog_configuration():

    config_location = "/etc/graylog/server/server.conf"
    configuration = None

    try:
        with open(config_location) as conf_file:
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
    c_root_password = False
    c_password_secret = False
    c_is_master = False
    c_rest_listen = False
    c_rest_transport = False
    c_web_listen = False
    c_elastic_max_index = False
    c_elastic_max_time = False

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
            if line.find("root_password_sha2 =") != -1 and not c_root_password:
                configuration[index] = "root_password_sha2 = " + pwd_hash.hexdigest() + "\n"
                log("INFO", "root_password_sha2 changed to: " + pwd_hash.hexdigest())
                c_root_password = True
            if line.find("password_secret =") != -1 and not c_password_secret:
                configuration[index] = "password_secret = " + pw_pepper + "\n"
                log("INFO", "changed password_secret to: " + pw_pepper)
                c_password_secret = True
            if line.find("is_master = ") != -1 and not c_is_master:
                configuration[index] = "is_master = " + is_master + "\n"
                log("INFO", "changed is_master to: " + is_master)
                c_is_master = True
            if line.find("rest_listen_uri = ") != -1 and not c_rest_listen:
                configuration[index] = "rest_listen_uri = http://" + web_ip + ":9000/api/" + "\n"
                log("INFO", "changed rest_listen_uri to: http://" + web_ip + ":9000/api/")
                c_rest_listen = True
            if line.find("rest_transport_uri = ") != -1 and not c_rest_transport:
                configuration[index] = "rest_transport_uri = http://" + web_ip + ":9000/api/" + "\n"
                log("INFO", "changed rest_transport_uri to: http://" + web_ip + ":9000/api/")
                c_rest_transport = True
            if line.find("web_enable = ") != -1 and not web_enable_found:
                configuration[index] = "web_enable = " + web_enable + "\n"
                web_enable_found = True
            if line.find("web_listen_uri = ") != -1 and not c_web_listen:
                configuration[index] = "web_listen_uri = http://" + web_ip + ":9000/" + "\n"
                log("INFO", "changed web_listen_uri to: http://" + web_ip + ":9000/")
                c_web_listen = True
            if line.find("elasticsearch_max_time_per_index = ") and not c_elastic_max_time:
                configuration[index] = "elasticsearch_max_time_per_index = 1d" + "\n"
                log("INFO", "changed elasticsearch_max_time_per_index to: 1d")
                c_elastic_max_time = True
            if line.find("elasticsearch_max_number_of_indices = ") and not c_elastic_max_index:
                configuration[index] = "elasticsearch_max_number_of_indices = " + log_retention + "\n"
                log("INFO", "changed elasticsearch_max_number_of_indices to: " + log_retention)
                c_elastic_max_index = True

        if not web_enable_found:
            configuration.append("web_enable = " + web_enable + "\n")
            log("INFO", "changed web_enable to: " + web_enable)

        all_config = {
            "c_root_password": c_root_password,
            "c_password_secret": c_password_secret,
            "c_is_master": c_is_master,
            "c_rest_listen": c_rest_listen,
            "c_rest_transport": c_rest_transport,
            "c_web_listen": c_web_listen,
            "c_elastic_max_index": c_elastic_max_index,
            "c_elastic_max_time": c_elastic_max_time
        }

        for key in all_config:
            if not all_config[key]:
                log("WARNING", "(Default value remains) Value not changed for: " + key)

        conf_file = open(config_location, 'w')
        conf_file.truncate()
        conf_file.writelines("".join(configuration))
    except TypeError:
        log('ERROR', "Expected string input, cannot parse input for config file.")
    except NameError as e:
        print e
        #log('ERROR', e)
    except IOError:
        log('ERROR', "changing admin password failed.")


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "--config":
            graylog_configuration()
    else:
        # change ip, dns, gateway and hostname settings
        # deprecated for now.
        # configure_host()

        # install openjdk-x-jre-
        openjdk_install()

        # install mongodb-server
        mongodb_install()

        # install elasticsearch
        elasticsearch_install()

        # make configuration changes to elasticsearch database
        elasticsearch_configuration()

        # install graylog-server
        graylog_install()

        # make configuration changes
        graylog_configuration()



