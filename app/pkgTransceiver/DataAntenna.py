#!/usr/bin/env python
'''
Handles the travel of data of already accepted Assistance Tasks
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import zipfile
# ASSISTANCE MODULE IMPORTS ----------
from AssistanceGenericAntenna import AssistanceGenericAntenna
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import SYMBOL_SEPARATOR,\
    STATUS_READY, STATUS_SENDING_DATA, STATUS_FINISHED, STATUS_GATHERING_DATA,\
    STATUS_DATA_READY, TIME_DATA_SERVER_INTERVAL, CHANNEL_FTP, CHANNEL_IMMEDIATE,\
    TYPE_STATUS_CHECK_MSG, TYPE_RECOVER_RESULTS_ANS, TYPE_RECOVER_RESULTS_MSG,\
    TYPE_DATA_SUBMIT_MSG, DIR_APPS_CWD, CHANNEL_ZIP_FTP


class DataAntenna (AssistanceGenericAntenna):
    '''
    Handles the traffic of data between peers with already accepted Assistance Tasks  # @IgnorePep8
    Must handle threats and etc
    '''

    def getTask(self, ticket):
        '''
        Returns the TaskDescription object with the given ticket
        :param ticket: ticket to search for the TaskDescription object
        '''
        return self.server.Instance.getOfficerInstance().getTask(ticket)  # @IgnorePep8

    def transceiverLOG(self, message, timeReceived, token, ticket, status):  # @IgnorePep8
        '''
        Logs the current situation to the transceiver's LOG
        :param message: message to be logged
        :param token: token received
        :param timeReceived: time the message was received
        :param ticket: the ticket included in the received message
        :param status: the status of the task with the received ticket
        '''
        logMsg = '\n' + str(message) + str(token)\
            + ";\n\ton port " + str(self.client_address[0])\
            + ";\n\tat: " + str(timeReceived)\
            + ";\n\tfor Assistance ServiceTicket " + str(ticket)\
            + ";\n\twhose status was: '" + str(status) + "' ;"
        if True:
            print logMsg
        self.server.Instance.getTransceiverInstance().logEvent(  # @IgnorePep8
            logMsg)

    def handleStatusCheck(self, timeReceived, authToken):
        '''
        Handles a message checking the status of a task
        :param timeReceived: the time the status check message was received
        :param authToken: the token of the message received
        '''
        ticket2check = self.rfile.readline().strip()
        task = self.getTask(ticket2check)
        self.transceiverLOG("Assistance DataTransfer Server: received an AssistanceStatusCheck message\n\tfrom API token ", # @IgnorePep8
                            timeReceived, authToken, ticket2check, task.STATUS)
        self.wfile.write(self.localToken + '\n'
                         + TYPE_RECOVER_RESULTS_ANS + '\n'
                         + ticket2check + '\n'
                         + task.STATUS + '\n')

    def handleRecoverResults(self, timeReceived, authToken):
        '''
        Handles a message requiring data. Holds until the data is ready,
        and sends the app's STDOUT and STDERR
        :param timeReceived: THe time the request was received
        :param authToken: the token of the requester
        '''
        ticket2check = self.rfile.readline().strip()
        task = self.getTask(ticket2check)
        self.transceiverLOG("Assistance DataTransfer Server: received an Assistance RecoverResults message\n\tfrom API token ", # @IgnorePep8
                            timeReceived, authToken,
                            ticket2check, task.STATUS)
        while task.STATUS != STATUS_READY:
            task = self.getTask(ticket2check)
            time.sleep(TIME_DATA_SERVER_INTERVAL)
        # outputs the data of the task
        if task.ANSWER_CHANNEL == CHANNEL_FTP:
            task.updateStatus(STATUS_SENDING_DATA)
            try:
                with open(task.STDOUT, 'rb') as stdoutFile:
                    while True:
                        fileData = stdoutFile.read()
                        if fileData == '':
                            break
                        self.request.sendall(fileData)
            except IOError:
                self.request.sendall("No STDOUT generated!")
            self.request.sendall(SYMBOL_SEPARATOR)
            with open(task.STDERR, 'rb') as stderrFile:
                while True:
                    fileData = stderrFile.read()
                    if fileData == '':
                        break
                    self.request.sendall(fileData)
            task.updateStatus(STATUS_FINISHED)
        else:
            self.wfile.write(self.localToken + '\n'
                             + TYPE_RECOVER_RESULTS_ANS + '\n'
                             + ticket2check + '\n'
                             + CHANNEL_IMMEDIATE + '\n'
                             + task.STDOUT + '\n'
                             + task.STDERR + '\n')
        return ticket2check

    def handleDataSubmit(self, timeReceived, authToken):
        '''
        Handles a message informing an impending data submission
        :param ticket2check: ticket of the task that is submitting data
        '''
        ticket = self.rfile.readline().strip()
        task = self.getTask(ticket)
        self.transceiverLOG("Assistance DataTransfer Server: received an AssistanceStatusCheck message\n\tfrom API token ", # @IgnorePep8
                            timeReceived, authToken,
                            ticket, task.STATUS)
        while task.STATUS != STATUS_GATHERING_DATA:
            task = self.getTask(ticket)
            time.sleep(TIME_DATA_SERVER_INTERVAL)
        # recovers the file name to be saved,
        # and its size must have already been sent on the message writeahead
        # print "receiving "+str(len(task.DATA_DELIVERY))+" files"
        for fileNum in range(len(task.DATA_DELIVERY)):
            fileName = self.rfile.readline().strip()
            # print "receiving file "+str(fileNum)+", "+fileName
            task.DATA_FILES.append(DIR_APPS_CWD + task.TICKET + '/' + fileName)
        # recovers the data of the file, and saves it to a file
        for fileNum in range(len(task.DATA_FILES)):
            with open(task.DATA_FILES[fileNum], 'wb') as dataFile:
                while True:
                    recoveredData = self.rfile.readline()
                    if recoveredData == '':
                        break
                    else:
                        dataFile.write(recoveredData)
        if task.DATA_CHANNEL == CHANNEL_ZIP_FTP:
            for fileNum in range(len(task.DATA_DELIVERY)):
                with zipfile.ZipFile(task.DATA_FILES[fileNum]) as zipf:
                    zipf.extractall(DIR_APPS_CWD + task.TICKET + '/')
                    task.DATA_FILES = []
                    for fileName in zipf.namelist():
                        task.DATA_FILES.append(DIR_APPS_CWD+task.TICKET+'/'+fileName)  # @IgnorePep8
        # updates the task data location and status
        # and unlocks the task's setup thread
        task.updateStatus(STATUS_DATA_READY)
        task.lock.set()

    def handle(self):
        '''
        Handles a new connection, parsing it header, dealing with threats,
        choosing the proper way to handle the data-related request
        and breaking it if it fails!
        '''
        try:
            self.localToken = self.server.Instance.getToken()
            timeReceived = time.time()
            msgType, authToken = self.parseMessageHeader()
            # check the kind of message we are dealing with, and deal accordingly @IgnorePep8
            # handles the message to check the status
            if msgType == TYPE_STATUS_CHECK_MSG:
                self.handleStatusCheck(timeReceived, authToken)

            # handle the message to recover the results
            elif msgType == TYPE_RECOVER_RESULTS_MSG:
                self.handleRecoverResults(timeReceived, authToken)

            # if this is a message to submit a file
            elif msgType == TYPE_DATA_SUBMIT_MSG:
                self.handleDataSubmit(timeReceived, authToken)

            else:
                errorString = "Assistance DataTransfer Server ERROR: Message of the wrong type sent to Assistance DataTransfer Server!\tMessage Type received: '"+msgType+'\n'  # @IgnorePep8
                self.wfile.write(errorString)
                raise ValueError(errorString)
        except IOError as ioerr:
            message = "I/O error({0}): {1}".format(ioerr.errno, ioerr.strerror)
            print message
