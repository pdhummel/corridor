from __future__ import print_function
import sys


class Logger:
    output_console = False

    def __init__(self):
        pass                            



def log(*vargs):
    if Logger.output_console:
        for arg in vargs:
            #sys.stdout.write(str(arg)
            print(arg, end=" ")
        print("", end="\n")