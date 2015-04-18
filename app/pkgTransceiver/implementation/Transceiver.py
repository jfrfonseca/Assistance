#!/usr/bin/env python
'''
Object to hold and run the antennas for all socket communications
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import datetime
import time
# ASSISTANCE MODULE IMPORTS ----------
from AssistanceSockets import AssistanceSocketServer
from APIRequestAntenna import APIRequestAntenna
from DataAntenna import DataAntenna
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import PORT_API_REQUESTS,\
    PORT_DATA_REQUESTS


class Transceiver():
    '''
    Handles all the socket input and output of the Assistance System
    '''
    # LOG of the Transceiver's interactions
    LOG = ""

    def logEvent(self, logMessage):
        '''
        Log an event to the Transceiver's LOG
        :param logMessage: Message to be logged
        '''
        self.LOG += "\n"+datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" "+logMessage

    def __init__(self):
        '''
        Starts the Transceiver by starting all the antennas
        '''
        self.LOG += "\n---------------- Assistance TRANSCEIVER service started up at "\
            +datetime.datetime.fromtimestamp( # @IgnorePep8
                time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" ----------------\n"  # @IgnorePep8
        self.apiRequestAntenna = AssistanceSocketServer(
            PORT_API_REQUESTS, APIRequestAntenna)
        self.dataAntenna = AssistanceSocketServer(
            PORT_DATA_REQUESTS, DataAntenna)

    def shutdown(self):
        '''
        Stops the transceiver by shutting down all of the antennas. Please use.
        '''
        self.apiRequestAntenna.shutdown()
        self.dataAntenna.shutdown()
        print "Transceiver is Off"
