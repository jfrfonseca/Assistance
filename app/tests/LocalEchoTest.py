from cpnLibrary.implementation.AssistanceDBMS import TOKEN_TRANSCEIVER_TEST,\
    TYPE_API_REQUEST_MSG, AppID_LOCAL_ECHO_TEST, NOT_APPLYED, PORT_API_REQUESTS,\
    TYPE_STATUS_CHECK_MSG, PORT_DATA_REQUESTS, TYPE_RECOVER_RESULTS_MSG, STATUS_READY,\
    TYPE_RECOVER_RESULTS_ANS
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time


def request(messageToEcho):
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_API_REQUEST_MSG+'\n'
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
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
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
        header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
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