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
scheduling = ''


def shutdown():
    '''
    Closes down all running threads and services of the system
    '''
    global transceiver
    transceiver.shutdown()


def setup(schedulingMode):
    '''
    Boots up the system
    '''
    global transceiver
    global officer
    global performer
    global scheduling
    officer = Officer()
    officer.scheduler.start()
    transceiver = Transceiver()
    scheduling = schedulingMode


def getTransceiverInstance():
    '''
    returns the running instance of the Transceiver
    '''
    global transceiver
    return transceiver


def getOfficerInstance():
    '''
    Returns the running instance of the Officer
    '''
    global officer
    return officer


def getSchedulingMode():
    return scheduling
