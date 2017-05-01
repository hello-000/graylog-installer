from logging import *


def create_cert():
    # change /etc/ssl/openssl.cnf

    opensslconfig_location = "/etc/ssl/openssl.cnf"

    try:
        with open(opensslconfig_location) as sslconf:
            sslconfiguration = sslconf.readlines()
        log("INFO", "reading " + opensslconfig_location)
        for index, line in enumerate(sslconfiguration):
            if line.find("#req_extensions = v3_req # The extensions to add to a certificate request"):
                sslconfiguration[index] = "req_extensions = v3_req # The extensions to add to a certificate request"
            if line.find("[ v3_req ]"):
                sslconfiguration[index + 1] = "subjectAltName = @alt_names"

    except IOError:
        log("ERROR", "Failed reading " + opensslconfig_location)

    print "OK"
    # create certs
