from Modules.logging import *
import subprocess

def import_cert():

    paths = ["/etc/default/cacerts", "/etc/ssl/certs/java/cacerts"]

    for path in paths:
        if subprocess.check_call(["keytool", "-importcert", "-keystore", path, "-storepass", "changeit", "-alias", "graylog-self-signed", "-file", "/etc/graylog/certs/graylog-certificate.pem"]) != 0:
            log("ERROR", "Cannot import certificate to store: " + path)
        else:
            log("INFO", "Successfully imported certificate to store: " + path)
