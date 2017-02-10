
from logging import *
from openjdk_installer import *


def graylog_database_install():
    if subprocess.check_call(["wget", "-qO", "elastickey", "https://packages.elastic.co/GPG-KEY-elasticsearch"]) != 0:
        log("ERROR", "Cannot retrieve elasticsearch package key.")

    if subprocess.check_call(["apt-key", "add", "elastickey"]) != 0:
        log("ERROR", "Cannot add elastickey to trusted keys")

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
    config_location = '/etc/elasticsearch/elasticsearch.yml'
    configuration = None

    try:
        with open(config_location) as conf_file:
            configuration = conf_file.readlines()
        log("INFO", "reading " + config_location)
    except:
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

    print "OK"


def main(args):
    if (args[1] == "--config"):
        database_configuration()
    else:
        # install dependencies Java, pwgen etc.
        openjdk_install()

        # install the elasticsearch database
        graylog_database_install()

        # make configuration change to the database config
        database_configuration()

main(sys.argv)
