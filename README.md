# graylog-installer

## graylog-server-installer
This python script will install:
	openjdk-x-jre (java 8 or above)
	mongodb-server
	graylog-server
    graylog-web (included in above package)

A separate script will be used for installing elasticsearch,
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
	elasticsearch

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
