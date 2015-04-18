#!/usr/bin/env python
'''
Starts the Assistance Service, and returns the running instances of its objects
Jose F. R. Fonseca
See Attached License file
'''
# ASSISTANCE MODULE IMPORTS ----------
from pkgTransceiver.implementation.Transceiver import Transceiver
from pkgOfficer.implementation.Officer import Officer

# ====================
# ------------------ Objects ------------------
# ====================
global transceiver
global officer
global performer


def shutdown():
    '''
    Closes down all running threads and services of the system
    '''
    global transceiver
    transceiver.shutdown()


def setup():
    '''
    Boots up the system
    '''
    global transceiver
    global officer
    global performer
    global assistanceAppRootDirectory
    officer = Officer()
    transceiver = Transceiver()


def getTransceiverInstance():
    '''
    returns the running instance of the Transceiver
    '''
    global transceiver
    return transceiver


def getOfficerInstance():
    '''
    Returns the running istance of the Officer
    '''
    global officer
    return officer
