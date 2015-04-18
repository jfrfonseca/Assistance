#!/usr/bin/env python
'''
Handles the distribution of the file, the ordering and initiating of the tasks,
and requests for remote executions
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import datetime
import threading
import hashlib
import SystemStats
import os.path
from random import randint
# ASSISTANCE MODULE IMPORTS ----------
from cpnLibrary.implementation.AssistanceDBMS import getThresholds,\
    getTaskPriority, getCallerScript
from pkgPerformer.implementation import Performer
from pkgOfficer.implementation.TaskDescription import TaskDescription
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import STATUS_WAITING, STATUS_REJECTED,\
    STATUS_GATHERING_DATA, STATUS_STANDBY, STATUS_READY, STATUS_DATA_READY,\
    TOKEN_TESTS_VERSION, NULL, DIR_LOGS, CHANNEL_FTP,\
    CHANNEL_LOCAL_FILE, DIR_APPS_CWD


class Officer():
    '''
Handles the distribution of the file, the ordering and initiating of the tasks,
and requests for remote executions
    '''
    '''
    BUFFER THAT CONTAINS ALL THE NON-FINISHED TASKS
    '''
    taskBuffer = {}

    def include(self, taskDescription):
        '''
Includes a new, still drafted task to the buffer,
decides if will perform the task or not
        :param taskDescription: The draft task to be evaluated
        '''
        ticket = self.generateTicket(taskDescription)
        self.taskBuffer[ticket] = taskDescription
        taskDescription.TICKET = ticket
        if self.decide(ticket):
            taskDescription.updateStatus(STATUS_WAITING)
            taskDescription.workerThreads["director"] = threading.Thread(
                target=self.setup, args=(ticket, ))
            taskDescription.workerThreads["director"].start()
            return ticket
        else:
            taskDescription.updateStatus(STATUS_REJECTED)
            # #TODO add task to dead archive
            return NULL

    def generateTicket(self, taskDescription):
        '''
Generates a new ServiceTicket to the most recent task received and processed
The TICKET must be the TIME_LABELED (time.time() defined here, 9.2 digits),
appended to 4 random digits,
appended to the (#TODO signed) SHA256 of the task's
    TIME_LABELED, localInstanceAuthToken, task's TOKEN, APPID,
    ARGUMENTS, DATA_DELIVERY
        :param taskDescription: The task to have the ticket created on
    '''
        tokenHash = hashlib.sha256()
        taskDescription.TIME_LABELED = time.time()

        tokenHash.update(str(taskDescription.TIME_LABELED))
        tokenHash.update(TOKEN_TESTS_VERSION)
        tokenHash.update(taskDescription.TOKEN)
        tokenHash.update(taskDescription.APPID)
        tokenHash.update(taskDescription.ARGUMENTS)
        tokenHash.update(taskDescription.DATA_DELIVERY)

        # the 4 random digits below are here to avoid that
        # two equal tasks from the same source at the same time
        # do not share a ticket value!
        randomQuartet = str(randint(0, 9999))
        while len(randomQuartet) < 4:
            randomQuartet = '0'+randomQuartet

        return str(taskDescription.TIME_LABELED).replace(".", "")\
            + randomQuartet\
            + str(tokenHash.hexdigest())

    def getTask(self, ticket):
        '''
        GETTER TO THE TASK BUFFER
        :param ticket: the ticket of the task to be recovered
        '''
        if ticket in self.taskBuffer.keys():
            return self.taskBuffer[ticket]
        else:
            # #TODO check the dead archive
            return TaskDescription(NULL, NULL, NULL, NULL, NULL, NULL, NULL)

    def decide(self, ticket):  # @UnusedVariable
        '''
        Decides if this instance will attend to the task or not
        Still a STUB
        :param ticket:
        '''
        return True

    def enoughLocalResources(self, ticket):
        '''
        Checks if there are enough resources to run the task of the given ticket  # @IgnorePep8
        :param ticket: ticket of the task to be evaluated
        '''
        locallyAvailable = True
        task = self.getTask(ticket)
        thresholds = getThresholds(task)
        memoryStatus = SystemStats.getMemoryUsage()
        CPUstatus = SystemStats.getCPUusage()
        CPUtotal = 0
        for index in range(len(CPUstatus)):
            CPUtotal += CPUstatus[index]
        CPUtotal /= len(CPUstatus)
        diskStatus = SystemStats.getFreeKbInAssistanceAppsCWD()
        task.logResourcesStatus({
            "memory": memoryStatus,
            "CPU": CPUtotal,
            "space": SystemStats.getFreeSpaceInAssistanceAppsCWD_HumanReadable()})  # @IgnorePep8
        if CPUtotal > thresholds["performLocal"]["CPU"]:
            locallyAvailable = False
            for memoryKind in memoryStatus.keys():
                if memoryStatus[memoryKind] > thresholds["performLocal"]["memory"][memoryKind]:  # @IgnorePep8
                    locallyAvailable = False
        if diskStatus < thresholds["performLocal"]["disk"]:
            locallyAvailable = False
        task.PROCESS_PRIORITY = getTaskPriority(task, CPUtotal, memoryStatus, diskStatus)  # @IgnorePep8
        return locallyAvailable

    def setup(self, ticket):
        '''
        Prepares and starts the execution of a task
        :param ticket: Ticket of the task to be run
        '''
        task = self.getTask(ticket)
        if self.enoughLocalResources(ticket):
            task.updateStatus(STATUS_GATHERING_DATA)
            if task.DATA_CHANNEL == CHANNEL_LOCAL_FILE:
                task.DATA_LOCATION = os.path.relpath(
                    task.DATA_DELIVERY, os.getcwd())
                task.updateStatus(STATUS_DATA_READY)
            elif task.DATA_CHANNEL == CHANNEL_FTP:
                task.DATA_LOCATION = DIR_APPS_CWD+'data/'
                task.lock.wait()
                task.lock.clear()
            else:
                task.updateStatus(STATUS_DATA_READY)
            task.SCRIPT = getCallerScript(task)
            task.updateStatus(STATUS_STANDBY)
            Performer.perform(task)
        # if it will be performed remotely, #TODO request remote assistance

        task.lock.wait()
        task.updateStatus(STATUS_READY)

    # DevTools methods ----------------------------------------
    def printLogs(self):
        '''
        Prints all the tasks logs on screen
        '''
        print "\n====================================\nLogs for all Assistance ServiceTickets in the Officer's Buffers as in "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')  # @IgnorePep8
        for ticket in self.taskBuffer.keys():
            print "ServiceTicket "+str(ticket)+" ("+self.getTask(ticket).STATUS+") Log:\n"+self.getTask(ticket).LOG  # @IgnorePep8

    def saveLogs(self):
        '''
        Saves all the tasks logs to a log file
        '''
        logTime = time.time()
        logFile = open(DIR_LOGS+str(int(time.time()))+".log", 'w')
        logFile.write("\n====================================\nLogs for all Assistance ServiceTickets in the Officer's Buffers as in "+datetime.datetime.fromtimestamp(logTime).strftime('%Y-%m-%d %H:%M:%S:%f'))  # @IgnorePep8
        for ticket in self.taskBuffer.keys():
            logFile.write("\nServiceTicket "+str(ticket)+" ("+self.getTask(ticket).STATUS+") Log:\n"+self.getTask(ticket).LOG)  # @IgnorePep8
        logFile.close()
