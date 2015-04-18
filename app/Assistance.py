#!/usr/bin/env python
'''
Assistance System API
Jose F. R. Fonseca
See Attached License file
'''
# ASSISTANCE MODULE IMPORTS ----------
from pkgMissionControl.implementation import Launcher


def shutdown():
    '''
    Shuts down the active Assistance Components
    '''
    Launcher.shutdown()


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
