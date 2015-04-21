#!/usr/bin/env python
'''
Assistance System API
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import zipfile
import os
# ASSISTANCE MODULE IMPORTS ----------
from pkgMissionControl.implementation import Launcher
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import DIR_APPS_CWD


def shutdown(cleanUp=False):
    '''
    Shuts down the active Assistance Components
    '''
    Launcher.shutdown()
    for dirType in ["data/", "outputs/"]:
        if cleanUp:
            filelist = os.listdir(DIR_APPS_CWD+dirType) # @IgnorePep8
            for f in filelist:
                os.remove(DIR_APPS_CWD+dirType+f)


def setup():
    '''
    Starts the Assistance Service
    '''
    Launcher.setup()

'''
Starts this file, if run independently
'''
if __name__ == '__main__':
    setup()
