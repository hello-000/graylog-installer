from logging import *
import sys
import signal
import os
import subprocess


def elasticsearch_configuration():
    config_location = '/etc/elasticsearch/elasticsearch.yml'
    configuration = None

    c_cluster_name = False
    c_network_host = False
    c_node_master = False
    c_node_data = False
    c_transport = False
    c_http = False
    c_multicast = False
    c_ping_unicast = False

    try:
        with open(config_location) as conf_file:
            configuration = conf_file.readlines()
        log("INFO", "reading " + config_location)
    except IOError:
        log('ERROR', "Failed reading " + config_location)

    sys.stdout.write("ip-address (elasticsearch server): ")
    network_host = raw_input()

    sys.stdout.write("node master? (y/n): ")
    is_master = raw_input()

    if is_master[0] == 'y':
        is_master = 'true'
    else:
        is_master = 'false'

    sys.stdout.write("data node? (y/n): ")
    data_node = raw_input()

    if data_node[0] == 'y':
        data_node = 'true'
    else:
        data_node = 'false'

    for index, line in enumerate(configuration):
        if line.find("cluster.name: ") != -1 and not c_cluster_name:
            configuration[index] = "cluster.name: graylog" + "\n"
            log("INFO", "cluster.name changed to graylog")
            c_cluster_name = True
        if line.find("network.host") != -1 and not c_network_host:
            configuration[index] = "network.host: " + network_host + "\n"
            log("INFO", "network.host changed to " + network_host)
            c_network_host = True
        if line.find("node.master: ") != -1 and not c_node_master:
            configuration[index] = "node.master: " + is_master + "\n"
            log("INFO", "node.master changed to " + is_master)
            c_node_master = True
        if line.find("node.data: ") != -1 and not c_node_data:
            configuration[index] = "node.data: " + data_node + "\n"
            log("INFO", "node.data changed to " + data_node)
            c_node_data = True
        if line.find("transport.tcp.port: ") != -1 and not c_transport:
            configuration[index] = "transport.tcp.port: 9300" + "\n"
            log("INFO", "transport.tcp.port changed to 9300")
            c_transport = True
        if line.find("http.port: ") != -1 and not c_http:
            configuration[index] = "http.port: 9200" + "\n"
            log("INFO", "http.port changed to 9200")
            c_http = True
        if line.find("discovery.zen.ping.multicast.enabled: ") != -1 and not c_multicast:
            configuration[index] = "discovery.zen.ping.multicast.enabled: false" + "\n"
            log("INFO", "discovery.zen.ping.multicast.enabled changed to false")
            c_multicast = True
        if line.find("discovery.zen.ping.unicast.hosts: ") != 1 and not c_ping_unicast:
            configuration[index] = "discovery.zen.ping.unicast.hosts: [\"" + network_host + "\", \"127.0.0.1\"]" + "\n"
            log("INFO", "discovery.zen.ping.unicast.hosts: [\"" + network_host + "\", \"127.0.0.1\"]")
            c_ping_unicast = True

    all_changed = {
        "c_cluster_name": c_cluster_name,
        "c_network_host": c_network_host,
        "c_node_master": c_node_master,
        "c_node_data": c_node_data,
        "c_transport": c_transport,
        "c_http": c_http,
        "c_multicast": c_multicast,
        "c_ping_unicast": c_ping_unicast
    }

    for key in all_changed:
        if all_changed[key] == False:
            log("WARNING", "No change made to " + key + " default config value remains.")

    conf_file = open(config_location, 'w')
    conf_file.truncate()
    conf_file.writelines("".join(configuration))
    conf_file.close()

    elasticsearch_dir = "/usr/share/elasticsearch/bin/"

    try:
        pidfile = open(elasticsearch_dir + "pidfile", "rw")
        pid = pidfile.readlines()

        if pid[0] != '':
            os.kill(int(pid[0]), signal.SIGTERM)
            try:
                os.kill(int(pid[0]), 0)
                log("WARNING", "Cannot kill elasticsearch proccess (pid " + pid[0] + ")")
            except OSError:
                log("INFO", "Elasticsearch processed successfully stopped")
        pidfile.close()
    except IOError:
        log("WARNING", "Cannot find pidfile - assuming elasticsearch is not running")

    if subprocess.check_call([elasticsearch_dir + "elasticsearch", "-d", "-p", elasticsearch_dir + "pidfile"]) != 0:
        log("ERROR", "Cannot start the elasticsearch database")

    log("INFO", "Elasticsearch database successfully started")
