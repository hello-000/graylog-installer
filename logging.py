import sys


class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(severity, msg):

    if severity == 'ERROR':
        cprint(pcolors.FAIL, "[*][" + severity + "] - " + msg + "Exiting script execution")
        sys.exit(1)

    if severity == 'INFO':
        cprint(pcolors.OKGREEN, "[*][" + severity + "] - " + msg)

    if severity == 'WARNING':
        cprint(pcolors.WARNING, "[*][" + severity + "] - " + msg)


def cprint(color, msg):
    print color + msg + pcolors.ENDC
