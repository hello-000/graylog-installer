
import signal
import os

from logging import *
from openjdk_installer import *
from elasticsearch_installer import *


def database_configuration():
    config_location = '/etc/elasticsearch/elasticsearch.yml'
    configuration = None
    pidfile = None
    pid = None

    try:
        with open(config_location) as conf_file:
            configuration = conf_file.readlines()
        log("INFO", "reading " + config_location)
    except IOError:
        log('ERROR', "Failed reading " + config_location)

    sys.stdout.write("ip-address (elasticsearch server): ")
    network_host = raw_input()

    for index, line in enumerate(configuration):
        if line.find("cluster.name: ") != -1:
            configuration[index] = "cluster.name: graylog"
            log("INFO", "cluster.name changed to graylog")
        if line.find("network.host") != -1:
            configuration[index] = "network.host: " + network_host
            log("INFO", "network.host changed to " + network_host)
        if line.find("transport.tcp.port: ") != -1:
            configuration[index] = "transport.tcp.port: 9300"
            log("INFO", "transport.tcp.port changed to 9300")
        if line.find("http.port: ") != -1:
            configuration[index] = "http.port: 9200"
            log("INFO", "http.port changed to 9200")

    conf_file = open(config_location, 'w')
    conf_file.truncate()
    conf_file.writelines("".join(configuration))

    elasticsearch_dir = "/usr/share/elasticsearch/bin/"

    try:
        pidfile = open(elasticsearch_dir + "pidfile", "rw")
        pid = pidfile.readlines()

        if pid[0] != '':
            os.kill(int(pid[0]), signal.SIGTERM)
            try:
                os.kill(int(pid[0]), 0)
                log("ERROR", "Cannot kill elasticsearch proccess (pid " + pid[0] + ")")
            except OSError:
                log("INFO", "Elasticsearch processed successfully stopped")
    except IOError:
        log("WARNING", "Cannot find pidfile - assuming elasticsearch is not running")

    if subprocess.check_call([elasticsearch_dir + "elasticsearch", "-d", "-p", elasticsearch_dir + "pidfile"]) != 0:
        log("ERROR", "Cannot start the elasticsearch database")

    log("INFO", "Elasticsearch database successfully started")


def main(args):

    if len(args) > 1:
        if args[1] == "--config":
            database_configuration()
    else:
        # install dependencies Java, pwgen etc.
        openjdk_install()

        # install the elasticsearch database
        elasticsearch_install()

        # make configuration change to the database config
        database_configuration()


main(sys.argv)
