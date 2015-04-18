#!/usr/bin/env python
'''
Handles the travel of data of already accepted Assistance Tasks
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
# ASSISTANCE MODULE IMPORTS ----------
import pkgMissionControl.implementation.Launcher
from AssistanceGenericAntenna import AssistanceGenericAntenna
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import TOKEN_TESTS_VERSION, SYMBOL_SEPARATOR,\
    STATUS_READY, STATUS_SENDING_DATA, STATUS_FINISHED, STATUS_GATHERING_DATA,\
    STATUS_DATA_READY, TIME_DATA_SERVER_INTERVAL, CHANNEL_FTP, CHANNEL_IMMEDIATE,\
    TYPE_STATUS_CHECK_MSG, TYPE_RECOVER_RESULTS_ANS, TYPE_RECOVER_RESULTS_MSG,\
    TYPE_DATA_SUBMIT_MSG


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
        return pkgMissionControl.implementation.Launcher.getOfficerInstance().getTask(ticket)  # @IgnorePep8

    def transceiverLOG(self, message, token, timeReceived, ticket, status):
        '''
        Logs the current situation to the transceiver's LOG
        :param message: message to be logged
        :param token: token received
        :param timeReceived: time the message was received
        :param ticket: the ticket included in the received message
        :param status: the status of the task with the received ticket
        '''
        pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent(  # @IgnorePep8
            message+token
            + ";\n\ton port " + str(self.client_address[0])
            + ";\n\tat: " + str(timeReceived)
            + ";\n\tfor Assistance ServiceTicket " + str(ticket)
            + ";\n\twhose status was: '" + status + "' ;")

    def handleStatusCheck(self, timeReceived, authToken):
        '''
        Handles a message checking the status of a task
        :param timeReceived: the time the status check message was received
        :param authToken: the token of the message received
        '''
        ticket2check = self.rfile.readline().strip()
        task = self.getTask(ticket2check)
        self.transceiverLOG("Assistance DataTransfer Server: received an AssistanceStatusCheck message\n\tfrom API token ", # @IgnorePep8
                            authToken, timeReceived, ticket2check, task.STATUS)
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
                            authToken, timeReceived,
                            ticket2check, task.STATUS)
        while task.STATUS != STATUS_READY:
            task = self.getTask(ticket2check)
            time.sleep(TIME_DATA_SERVER_INTERVAL)
        # outputs the data of the task
        if task.ANSWER_CHANNEL == CHANNEL_FTP:
            stdoutFile = open(task.STDOUT, 'rb')
            stderrFile = open(task.STDERR, 'rb')
            stdout = stdoutFile.read()
            stderr = stderrFile.read()
            task.updateStatus(STATUS_SENDING_DATA)
            self.request.sendall(stdout)
            self.request.sendall(SYMBOL_SEPARATOR)
            self.request.sendall(stderr)
            task.updateStatus(STATUS_FINISHED)
            stdoutFile.close()
            stderrFile.close()
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
                            authToken, timeReceived,
                            ticket, task.STATUS)
        while task.STATUS != STATUS_GATHERING_DATA:
            task = self.getTask(ticket)
            time.sleep(TIME_DATA_SERVER_INTERVAL)
        # recovers the file name to be saved,
        # and its size must have already been sent on the message writeahead
        fileName = self.rfile.readline().strip()
        fileSize = int(task.DATA_DELIVERY)
        task.DATA_LOCATION = task.DATA_LOCATION + fileName
        # recovers the data of the file, and saves it to a file
        recoveredData = self.request.recv(fileSize)
        dataFile = open(task.DATA_LOCATION, 'wb')
        dataFile.write(recoveredData)
        dataFile.close()
        # updates the task data location and status
        # and unlocks the task's setup thread
        task.updateStatus(STATUS_DATA_READY)
        task.lock.set()

    def handle(self):
        '''
        Handles a new connection, parsing it header, dealing with threats,
        choosing the proper way to handle the data-related request
        '''
        self.localToken = TOKEN_TESTS_VERSION
        timeReceived = time.time()
        msgType, authToken = self.parseMessageHeader()
        # check the kind of message we are dealing with, and deal accordingly
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
