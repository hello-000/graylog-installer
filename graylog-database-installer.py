
from Modules.openjdk_installer import *
from Modules.elasticsearch_installer import *
from Modules.elasticsearch_configuration import *


def main(args):
    if len(args) > 1:
        if args[1] == "--config":
            elasticsearch_configuration()
    else:
        # install dependencies Java, pwgen etc.
        openjdk_install()

        # install the elasticsearch database
        elasticsearch_install()

        # make configuration change to the database config
        elasticsearch_configuration()


main(sys.argv)
