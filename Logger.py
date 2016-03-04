from __future__ import print_function
import sys
import logging


class Logger:
    output_console = True
    logging_configured = False

    def __init__(self):
        pass

def initialize():
    if Logger.output_console:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(filename='./corridor.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    Logger.logging_configured = True


def log(*vargs):
    if not Logger.logging_configured:
        initialize()
    output = ""
    for arg in vargs:
        #sys.stdout.write(str(arg)
        output = output + str(arg) + " "
    logging.debug(output)