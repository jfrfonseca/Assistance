import os
from pkgMissionControl.implementation import Launcher


def shutdown():
    Launcher.shutdown()
        

def setup():
    Launcher.setup()


def getCWD():
    return os.getcwd()
