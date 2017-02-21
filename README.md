# graylog-installer

## graylog-server-installer
This python script will install:
	openjdk-x-jre (java 8 or above)
	mongodb-server
	elasticsearch-client
	graylog-server
    graylog-web (included in above package)

A separate script will be used for installing elasticsearch-server,
as it is recommended to keep these two instances separate.
For further documentation on the installation of Graylog,
please refer to the official documentation:
    http://docs.graylog.org/en/2.1/pages/installation/os/ubuntu.html

Please be aware, that this script is written for Ubuntu 16.04
should it be installed on an Ubuntu 14.04, there are certain
changes that need to be made, before running the script, as
is no native support for java-8.

## graylog-database-installer
This python script will install:
	openjdk-x-jre (java 8 or above)
	elasticsearch-server

It it recommended to run this script first. as the graylog
server is dependent on the elasticsearch component on startup.
graylog-server-installer will finish the installation by starting
the graylog service, and will alarm if the database is unreachable.
In the case of this happening, please follow the instructions
presented by the warnings produced by the script. 

In other words, this will install the elasticsearch component
in a graylog setup. It is recommended by graylog to install
these components separately, but should there be a warrant
for installing web-interface, graylog-processor and database
on the same server, that is also possible.

In this case, the openjdk-x-jre will be skipped by
graylog-server-installer.

## Project Details

### graylog-server-installer

#### Network Configuration
    o   Has been deprecated, this must be done manually.
#### Java JDK
    o   Installed with defaults. This is running as intended.
#### MongoDB
    o   Currently installing with defaults
    o   This has to be changed to also include a mongo admin user, which is then
        also used to connect to the database by the graylog-server.
    o   No other current tasks on this section.
#### Elasticsearch
    o   Currently installing with defauls.
    o   Configuration made to the elasticsearch database is identical to the graylog-database-installer configuration
            v   cluster.name: graylog
            v   network.host <local-ip>
            v   transport.tcp.port: 9300 (default)
            v   http.port: 9200 (default)
            v   node.master
            v   node.data
            v   discovery.zen.multicast.enabled: false
            v   discovery.zen.ping.unicast.hosts: [<localip>, localhost]

    o   Configuration needed to be added:
            x   Need to add a user input for log retention
            x   multi-node cluster configuration

#### Graylog
    o   Currently installing 2.1 (This needs to be changed to 2.2) all defaults (intended)
    o   Currently Configuring:
            v   root_password_sha2 (admin password hash)
            v   password_secret (randomly generated)
            v   is_master
            v   rest_listen_uri (web ip)
            v   rest_transport_uri (web ip)
            v   web_enable
            v   web_listen_uri (web ip)
            v   elasticsearch_max_time_per_index (log retention)
            v   elasticsearch_max_number_of_indices (log retention)

    o   Configuration needed to be added:
            x   Need to add a user input for log retention
            x   multi-node cluster configuration

### graylog-database-installer

Short note, that for debugging reasons, a cmd line parameter --config has been included
in case that there is no need to install elasticsearch nor open-jdk, but the user is only interested
in the configuration part of this script.

#### Java JDK
    o   Installed with defaults. This is running as intended.
#### Elasticsearch
    o   Using the same installer as Graylog
    o   Currently Configuring:
        v   cluster.name: graylog
        v   network.host <local-ip>
        v   transport.tcp.port: 9300 (default)
        v   http.port: 9200 (default)
        v   node.master
        v   node.data
        v   discovery.zen.multicast.enabled: false
        v   discovery.zen.ping.unicast.hosts: [<localip>, localhost]

    o   Configuration needed to be added:
            v   multi-node cluster configuration
























