from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time
from cpnLibrary.implementation.Constants import *


def request(messageToEcho):
    header = TOKEN_LOCAL+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_LOCAL_ECHO_TEST+'\n'+messageToEcho+'\n'+NOT_APPLYED+'\n'+NOT_APPLYED+'\n'
    dummySocket = AssistanceSocketClient('', PORT_API_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+apiRequestMsg)
    #print "receiving ticket"
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[2]


def checkStatus(serviceTicket):
    header = TOKEN_LOCAL+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
    statusCheckMsg = serviceTicket+'\n'
    dummySocket = AssistanceSocketClient('', PORT_DATA_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+statusCheckMsg)
    #print "receiving ticket"
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[3]


def synchronise(serviceTicket):
    msgType = ""
    while not msgType == TYPE_RECOVER_RESULTS_ANS:
        header = TOKEN_LOCAL+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
        recoverMsg = serviceTicket+'\n'
        dummySocket = AssistanceSocketClient('', PORT_DATA_REQUESTS)
        #print "sending message"
        dummySocket.sendData(header+recoverMsg)
        #print "receiving ticket"
        answerData = dummySocket.receiveData()
        #print "closing socket"
        dummySocket.close()
        msgType = answerData.split('\n')[1]
    return answerData.split('\n')[4]