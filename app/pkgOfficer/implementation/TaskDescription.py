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
    STATUS_DRAFT, STATUS_WAITING


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
        self.PRO_LOG = '\n' + str(timeReceived) + '\t' + str(self.STATUS)
        self.TOKEN = authToken
        self.TIME_RECEIVED = timeReceived
        self.TIME_LABELED = NOT_APPLYED

        # Task Request Meta
        self.APPID = appID
        self.DATA_CHANNEL = appDataChannel
        # Task Request Data
        self.ARGUMENTS = appArgs
        self.DATA_DELIVERY = appDataDelivery
        self.DATA_FILES = []

        # Task Answer Meta
        self.answer = {}
        self.STDOUT = NULL
        self.STDERR = NULL
        self.ANSWER_CHANNEL = appAnswerChannel
        self.TIME_COMPLETED = NULL
        self.TIME_INTERRUPTED = NULL
        self.CHECKPOINT = NULL

        # Task Runtime Values
        self.SCRIPT = NULL
        self.workerThreads = {}
        self.lock = threading.Event()
        self.PROCESS_PRIORITY = NULL

    def updateStatus(self, newStatus):
        '''
        Updates and logs the status of the task
        :param newStatus: the new status of the task
        '''
        appendString = "\t"+datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')\
            + " |- Status update: (" + str(self.STATUS) + " --> " + str(newStatus) + ");\n"  # @IgnorePep8
        self.LOG += appendString
        self.PRO_LOG += '\n' + str(time.time()) + '\t' + str(newStatus)
        self.STATUS = newStatus

    def changePriority(self, newPriority):
        '''
        Changes the priority of the task, and logs this act
        :param newPriority: new priority of the task
        '''
        self.LOG += "\t"+datetime.datetime.fromtimestamp(
            time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')\
            + " |- Changed Local processing priority from "\
            + str(self.PROCESS_PRIORITY) + " to " + str(newPriority) + ");\n"
        self.PROCESS_PRIORITY = newPriority
        self.PRO_LOG += '\n' + str(time.time()) + '\t PRIORITY=' + str(self.PROCESS_PRIORITY)  # @IgnorePep8

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
        self.PRO_LOG += '\n' + str(time.time())\
            + '\t CPU=' + str(cpuMemDiskUsage["CPU"])\
            + '\t mem=' + str(cpuMemDiskUsage["memory"])\
            + '\t freeDisk=' + str(cpuMemDiskUsage["space"])

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

    def printOut(self):
        '''
        Prints the log of the task to the screen
        '''
        data = str(self.TICKET) + '\n' + str(self.TOKEN) + '\n' + str(self.TIME_RECEIVED) + '\n'\
            + str(self.APPID) + '\n'\
            + str(self.ARGUMENTS) + '\n' + str(self.DATA_FILES) + '\n'\
            + str(self.SCRIPT) + '\n' + str(self.STATUS) + '\n'\
            + str(self.TIME_COMPLETED) + '\n' + str(self.TIME_INTERRUPTED) + '\n'\
            + str(self.STDOUT) + '\n' + str(self.STDERR) + '\n' + str(self.PRO_LOG) + '\n'  # @IgnorePep8
        return data
