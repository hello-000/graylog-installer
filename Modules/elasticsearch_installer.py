from logging import *
import subprocess


def elasticsearch_install():
    if subprocess.check_call(["wget", "-qO", "elastickey", "https://packages.elastic.co/GPG-KEY-elasticsearch"]) != 0:
        log("ERROR", "Cannot retrieve elasticsearch package key.")

    if subprocess.check_call(["apt-key", "add", "elastickey"]) != 0:
        log("ERROR", "Cannot add elastickey to trusted keys")

    log("INFO", "Retrieved elasticsearch package key successfully")

    if subprocess.check_call(["echo", "deb https://packages.elastic.co/elasticsearch/2.x/debian stable main", "|", "sudo", "tee", "-a", "/etc/apt/sources.list.d/elasticsearch-2.x.list"]) != 0:
        log("ERROR", "Cannot add elasticsearch to /etc/apt/source.list.d/")

    log("INFO", "Added elasticsearch package to /etc/apt/source.list.d/ successfully")

    if subprocess.check_call(["apt-get", "update", "-y"]) != 0:
        log("ERROR", "Cannot install update apt-get.")

    if subprocess.check_call(["apt-get", "install", "-y", "elasticsearch"]) != 0:
        log("ERROR"" Cannot installed elasticsearch")

    log("INFO", "Installed elasticsearch successfully.")
