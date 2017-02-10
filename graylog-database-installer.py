
from logging import *
from openjdk_installer import *


def graylog_database_install():
    if subprocess.check_call(["wget", "-qO", "https://packages.elastic.co/GPG-KEY-elasticsearch", "|",  "sudo", "apt-key", "add", "-"]) != 0:
        log("ERROR", "Cannot retrieve elasticsearch package key.")

    log("INFO", "Retrieved elasticsearch package key successfully")

    if subprocess.check_call(["echo", "deb https://packages.elastic.co/elasticsearch/2.x/debian stable main", "|", "sudo", "tee", "-a", "/etc/apt/sources.list.d/elasticsearch-2.x.list"]) != 0:
        log("ERROR", "Cannot add elasticsearch to /etc/apt/source.list.d/")

    log("INFO", "Added elasticsearch package to /etc/apt/source.list.d/ successfully")

    if subprocess.check_call(["apt-get", "update"]) != 0:
        log("ERROR", "Cannot install update apt-get.")

    if subprocess.check_call(["apt-get", "install", "elasticsearch"]) != 0:
        log("ERROR"" Cannot installed elasticsearch")

    log("INFO", "Installed elasticsearch successfully.")


def database_configuration():
    configuration = None

    try:
        with open('server.conf') as conf_file:
            configuration = conf_file.readlines()
        log("INFO", "reading /etc/graylog/server/server.conf")
    except:
        log('ERROR', "Failed reading /etc/graylog/server/server.conf")

    print "OK"


def main():
    # install dependencies Java, pwgen etc.
    openjdk_install()

    # install the elasticsearch database
    graylog_database_install()

    # make configuration change to the database config
    # database_configuration()

main()
