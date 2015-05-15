#!/usr/bin/env python
'''
Receives and treats all new requests to the Assistance System
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
# ASSISTANCE MODULE IMPORTS ----------
from pkgOfficer.TaskDescription import TaskDescription
from AssistanceGenericAntenna import AssistanceGenericAntenna
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import TYPE_API_REQUEST_ANS, TYPE_API_REQUEST_MSG


class APIRequestAntenna (AssistanceGenericAntenna):
    '''
    Receives and treats all new requests to the Assistance System
    Must handle DoS and other threats
    '''

    def parseAssistanceRequest(self, authToken, timeReceived):
        '''
        In a running connection, reads the data of a new Assistance Request
        And uses it to mount a TaskDescription object
        :param authToken: The already parsed token of the peer
        :param timeReceived: The time the data was received
        '''
        appID = self.rfile.readline().strip()
        appArgs = self.rfile.readline().strip()
        appDataChannel = self.rfile.readline().strip()
        appDataDelivery = self.rfile.readline().strip().split(' ')
        appAnswerChannel = self.rfile.readline().strip()
        task = TaskDescription(authToken, timeReceived,
                               appID, appArgs,
                               appDataChannel, appDataDelivery,
                               appAnswerChannel)
        return task

    def handle(self):
        '''
        Creates a new Connection on socket connect, and parses the connection data,  # @IgnorePep8
        handles problems, etc
        '''
        timeReceived = time.time()
        msgType, authToken = self.parseMessageHeader()
        if msgType == TYPE_API_REQUEST_MSG:
            task = self.parseAssistanceRequest(authToken, timeReceived)
            ticket = self.server.Instance.getOfficerInstance().include(task)
            self.wfile.write(self.localToken+"\n"
                             + TYPE_API_REQUEST_ANS + "\n"
                             + ticket + "\n")
            logMessage = "\nReceived a new AssistanceRequest from " + str(authToken)\
                + ";\n\ton port " + str(self.client_address[0])\
                + ";\n\tat: " + str(timeReceived) + "' ;"
            if True:
                print logMessage
            self.server.Instance.getTransceiverInstance().logEvent(  # @IgnorePep8
                logMessage)

        else:
            errorString = "Assistance APIRequest Server ERROR: Message of the wrong type sent to Assistance APIRequest Server!\tMessage Type received: '"+msgType  # @IgnorePep8
            self.wfile.write(errorString)
            raise ValueError(errorString)
