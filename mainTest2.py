import pandas as pd
import os
import sys

class Tee(object):
    def __init__(self, file_name="output.log"):
        self.file = open(file_name, "a")

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, message):
        self.file.write(message)
        self.file.flush()
        self.stdout.write(message)


def checkOs():
    """
    Check system OS if windows change path syntax
    """
    if os.name == "nt":
        logPath = ".\\"