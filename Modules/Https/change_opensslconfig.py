from Modules.logging import *

LINE_BREAK = "\n"


def change_opensslconfig(ip_address):
    # change /etc/ssl/openssl.cnf

    sslconfiguration = None
    opensslconfig_location = "/etc/ssl/openssl.cnf"
    reqextensions_discovered = 0
    v3req_discovered = 0

    try:
        with open(opensslconfig_location) as sslconf:
            sslconfiguration = sslconf.readlines()
            log("INFO", "reading " + opensslconfig_location)
    except IOError:
        log("ERROR", "Failed reading " + opensslconfig_location)

    log("INFO", "log is working")

    for index, line in enumerate(sslconfiguration):
        # print "[" + str(index) + "]" + " - " + line
        if line.find("req_extensions = v3_req") != -1:
            log("INFO", " # req_extensions found on line " + str(index))
            sslconfiguration[index] = "req_extensions = v3_req # The extensions to add to a certificate request" + LINE_BREAK
            reqextensions_discovered = 1
        if line.find("[ v3_req ]") != -1:
            log("INFO", "[ v3_req ] found on line " + str(index))
            sslconfiguration[index + 1] = "subjectAltName = @alt_names" + LINE_BREAK
            sslconf_left = sslconfiguration[0:index + 2]
            sslconf_right = sslconfiguration[index + 2:]
            sslconf_left.append("[alt_names]" + LINE_BREAK)
            sslconf_left.append("IP.1 = " + ip_address + LINE_BREAK)
            v3req_discovered = 1
            sslconfiguration = sslconf_left + sslconf_right

    if reqextensions_discovered == 1 and v3req_discovered == 1:
        new_conffile = open(opensslconfig_location, 'w')
        new_conffile.truncate()
        new_conffile.writelines("".join(sslconfiguration))
        new_conffile.close()
        log("INFO", "SSL configuration successfully modified")
        return "SUCCESS"
    else:
        log("ERROR", "Could not modify SSL configuration successfully")
        return "ERROR"
