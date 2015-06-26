#!/usr/bin/env python
'''
Handles the distribution of the file, the ordering and initiating of the tasks,
and requests for remote executions
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import threading
import hashlib
from pkgOfficer import SystemStats
import os.path
from random import randint
# ASSISTANCE MODULE IMPORTS ----------
from pkgPerformer import Performer
from pkgOfficer.AssistanceRules import getThresholds, getTaskPriority, getCallerScript,\
    volunteer, schedule
from pkgOfficer import TaskDescription
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import STATUS_WAITING, STATUS_REJECTED,\
    STATUS_GATHERING_DATA, STATUS_STANDBY, STATUS_READY, STATUS_DATA_READY,\
    NULL, CHANNEL_FTP, CHANNEL_LOCAL_FILE, DIR_APPS_CWD, LOG_OFFICER, LOG_OFFICERHF,\
    STATUS_PERFORMING_LOCAL, CHANNEL_ZIP_FTP


class Officer():
    '''
Handles the distribution of the file, the ordering and initiating of the tasks,
and requests for remote executions
    '''

    def __init__(self, Instance):
        self.taskBuffer = {}
        self.schedulerLock = threading.Event()
        self.Instance = Instance
        self.SCHEDULING_ACTIVE = True
        self.scheduler = threading.Thread(target=schedule, args=(self,))  # @IgnorePep8
        self.scheduler.start()

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
        tokenHash.update(self.Instance.getToken())
        tokenHash.update(taskDescription.TOKEN)
        tokenHash.update(taskDescription.APPID)
        tokenHash.update(taskDescription.ARGUMENTS)
        for dataFile in taskDescription.DATA_DELIVERY:
            tokenHash.update(dataFile)

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

    def getStandbyTaskTickets(self):
        return [ticket for ticket in self.taskBuffer.keys()
                if self.getTask(ticket).STATUS == STATUS_STANDBY]

    def getPerformingTaskTickets(self):
        return [ticket for ticket in self.taskBuffer.keys()
                if self.getTask(ticket).STATUS == STATUS_PERFORMING_LOCAL]

    def decide(self, ticket):  # @UnusedVariable
        '''
        Recovers the decision to run or not a task, given its ticket
        :param ticket: ticket of the task to be decided
        '''
        task = self.getTask(ticket)
        answer = volunteer(task)
        return answer

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
            if task.DATA_CHANNEL == CHANNEL_LOCAL_FILE:
                task.updateStatus(STATUS_GATHERING_DATA)
                for dataFile in task.DATA_DELIVERY:
                    task.DATA_FILES.append(os.path.relpath(dataFile, os.getcwd()))  # @IgnorePep8
                task.updateStatus(STATUS_DATA_READY)
            elif task.DATA_CHANNEL == CHANNEL_FTP\
                    or task.DATA_CHANNEL == CHANNEL_ZIP_FTP:
                os.makedirs(DIR_APPS_CWD+task.TICKET)
                task.updateStatus(STATUS_GATHERING_DATA)
                task.lock.wait()
                task.lock.clear()
            else:
                task.updateStatus(STATUS_DATA_READY)
            task.SCRIPT = getCallerScript(task)
            task.updateStatus(STATUS_STANDBY)
            self.schedulerLock.set()
            task.lock.wait()
            task.lock.clear()
            Performer.perform(task)
            self.schedulerLock.set()
        # if it will be performed remotely, #TODO request remote assistance
        # waits until the data is sent to mark as finished
        task.lock.wait()
        task.updateStatus(STATUS_READY)
        with open(LOG_OFFICER+'.backup', 'a') as outerLOG:
            outerLOG.write("\n<BEGIN>\n" + task.printOut() + "<END>")

    def shutdown(self):
        self.SCHEDULING_ACTIVE = False
        self.schedulerLock.set()
        print "Officer Down"

    def saveLogs(self):
        '''
        Saves all the tasks logs to a log file
        '''
        logFileHF = open(LOG_OFFICERHF, 'w')
        with open(LOG_OFFICER, 'w') as logFile:
            for ticket in self.taskBuffer.keys():
                task = self.getTask(ticket)
                logFileHF.write("\n<BEGIN><TICKET=" + str(ticket)
                                + "><STATUS=" + task.STATUS
                                + ">\n"+task.LOG + "\n<END>")
                logFile.write("\n<BEGIN>\n" + task.printOut() + "<END>")
        logFileHF.close()
