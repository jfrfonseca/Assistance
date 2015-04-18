#!/usr/bin/env python
'''
Object that describes a task submitted to the Assistance System
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import datetime
import threading
import time
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import NOT_APPLYED, NULL,\
    STATUS_DRAFT, STATUS_WAITING, DIR_APPS_CWD


class TaskDescription():
    '''
    Class of the Object that describes a task submitted to the Assistance System  # @IgnorePep8
    '''
    def __init__(self,
                 authToken,
                 timeReceived,
                 appID,
                 appArgs,
                 appDataChannel, appDataDelivery,
                 appAnswerChannel):
        '''
        Creates the task with the provided arguments
        :param authToken: Token of the task's creator
        :param timeReceived: The time the task was received by the system
        :param appID: The ID of the app to be run
        :param appArgs: THe arguments of the app
        :param appDataChannel: The method that the data for the app will be sent  # @IgnorePep8
        :param appDataDelivery: The arguments of the data sending method
        :param appAnswerChannel: The method the answer must be sent back
        '''
        # Task General Meta
        self.TICKET = NOT_APPLYED
        self.STATUS = STATUS_DRAFT
        self.LOG = "\t"+datetime.datetime.fromtimestamp(timeReceived).strftime(
            '%Y-%m-%d %H:%M:%S:%f')\
            + " |- New task (APPID '" + str(appID)\
            + "') received by Assistance from token " + authToken + ";\n"
        self.TOKEN = authToken
        self.TIME_RECEIVED = timeReceived
        self.TIME_LABELED = NOT_APPLYED

        # Task Request Meta
        self.APPID = appID
        self.DATA_CHANNEL = appDataChannel
        # Task Request Data
        self.ARGUMENTS = appArgs
        self.DATA_DELIVERY = appDataDelivery
        self.DATA_LOCATION = NULL

        # Task Answer Meta
        self.answer = {}
        self.STDOUT = NULL
        self.STDERR = NULL
        self.ANSWER_CHANNEL = appAnswerChannel
        self.OUTPUT_DIR = DIR_APPS_CWD+"outputs/"
        self.TIME_COMPLETED = NULL
        self.TIME_INTERRUPTED = NULL
        self.CHECKPOINT = NULL

        # Task Runtime Values
        self.SCRIPT = NULL
        self.workerThreads = {}
        self.lock = threading.Event()
        self.PROCESS_PRIORITY = NULL

        self.onlineLog = False

    def updateStatus(self, newStatus):
        '''
        Updates and logs the status of the task
        :param newStatus: the new status of the task
        '''
        appendString = "\t"+datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')\
            + " |- Status update: (" + str(self.STATUS) + " --> " + str(newStatus) + ");\n"  # @IgnorePep8
        self.LOG += appendString
        self.STATUS = newStatus
        self.seeLog()

    def changePriority(self, newPriority):
        '''
        Changes the priority of the task, and logs this act
        :param newPriority: new priority of the task
        '''
        self.LOG += "\t"+datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')\
            + " |- Changed Local processing priority from "\
            + str(self.PROCESS_PRIORITY) + " to " + str(newPriority) + ");\n"
        self.STATUS = newPriority
        self.seeLog()

    def logResourcesStatus(self, cpuMemDiskUsage):
        '''
        Logs the current resources status of the host system
        :param cpuMemDiskUsage: the usage of each item of the host system
        '''
        self.LOG += "\t"+datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')\
            + " |- The current usage of system resources is: "
        self.LOG += "--free space (in AssistanceApps CWD partition): "\
            + str(cpuMemDiskUsage["space"]) + ";\t"
        self.LOG += "--memory usage: "+str(cpuMemDiskUsage["memory"])+"%;\t"
        self.LOG += "--CPU usage: "+str(cpuMemDiskUsage["CPU"])+"%;\n"
        self.seeLog()

    def setTicket(self, ticketValue):
        '''
        Sets the ticket of the task, prevents reseting, and logs it
        :param ticketValue: the ticket to be set
        '''
        if self.TICKET != NOT_APPLYED:
            raise ValueError(
                "Security Alert! Attempt to overwrite Assistance ServiceTicket of task TICKET "+str(self.TICKET)+"!")  # @IgnorePep8
        else:
            self.TICKET = ticketValue
            self.LOG += "\t"\
                + datetime.datetime.fromtimestamp(self.TIME_LABELED).strftime(
                    '%Y-%m-%d %H:%M:%S:%f') + " |- Assigned TICKET '"\
                + str(self.TICKET) + "';\n"
            self.updateStatus(STATUS_WAITING)
        self.seeLog()

    def seeLog(self):
        '''
        Prints the log of the task to the screen
        '''
        if self.onlineLog:
            print >> open('LOG/0000_onlineLog.dat', 'a'), self.TICKET, "\t", self.LOG  # @IgnorePep8
