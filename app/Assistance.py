#!/usr/bin/env python
'''
Assistance System API
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import os
import shutil
# ASSISTANCE MODULE IMPORTS ----------
from pkgTransceiver.Transceiver import Transceiver
from pkgOfficer.Officer import Officer
from IOUtils import saveAll
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import SCHEDULE_ROUNDROBIN


class Assistance():
    '''
    Mission Control and main Object for a instance of the Assistance System
    '''
    def __init__(self, schedulingMode=SCHEDULE_ROUNDROBIN, token="0123456789ABCDEF"):  # @IgnorePep8
        '''
        Initiates a new Assistance System Instance in the local Machine
        :param schedulingMode:
        '''
        self.token = token
        self.scheduling = schedulingMode
        self.officer = Officer(self)
        self.transceiver = Transceiver(self)

    def shutdown(self, zipName=''):
        '''
        Deactivates the current running instance of the Assistance System
        Saves the LOGs, shuts down the Office, shuts down the Trasnceiver, zips the LOGs  # @IgnorePep8
        AND deletes all the logs BUT the zipped ones!
        :param zipName: name to give for the ZIPfile logs, as LOGs-zipName-scheduleStrategy.zip  # @IgnorePep8
        '''
        self.officer.saveLogs()
        self.officer.shutdown()
        self.transceiver.shutdown()
        saveAll(zipName)
        dirs2Clean = ['LOG', 'AssistanceApps/runtimeIO']
        for folder in dirs2Clean:
            for root, dirs, files in os.walk(folder):  # @UnusedVariable
                for fileName in files:
                    os.remove(os.path.join(folder, fileName))
                for dirName in dirs:
                    shutil.rmtree(os.path.join(folder, dirName))

    def getTransceiverInstance(self):
        '''
        returns the running instance of the Transceiver
        '''
        return self.transceiver

    def getOfficerInstance(self):
        '''
        Returns the running instance of the Officer
        '''
        return self.officer

    def getSchedulingMode(self):
        '''
        Returns the used Scheduling mode
        '''
        return self.scheduling

    def getToken(self):
        return self.token
