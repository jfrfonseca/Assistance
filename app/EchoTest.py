from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time
from cpnLibrary.implementation.Constants import NULL, TOKEN_TESTS_VERSION,\
    AppID_LOCAL_ECHO_TEST, TYPE_API_REQUEST_MSG, PORT_API_REQUESTS,\
    TYPE_STATUS_CHECK_MSG, PORT_DATA_REQUESTS, STATUS_READY,\
    TYPE_RECOVER_RESULTS_MSG, CHANNEL_IMMEDIATE


HOST = ''


def request(messageToEcho, peerIP=HOST):
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_LOCAL_ECHO_TEST+'\n'+messageToEcho+'\n'+NULL+'\n'+NULL+'\n'+CHANNEL_IMMEDIATE+'\n'
    '''
    SEND
    '''
    print "requesting to "+str(peerIP)+":"+str(PORT_API_REQUESTS)
    dummySocket = AssistanceSocketClient(peerIP, PORT_API_REQUESTS)
    dummySocket.sendData(header+apiRequestMsg)
    '''
    GET TICKET
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    ticket = answerData.split('\n')[2]
    return ticket


def checkStatus(serviceTicket, peerIP=HOST):
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
    statusCheckMsg = serviceTicket+'\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(peerIP, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+statusCheckMsg)
    '''
    GET STATUS
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    status = answerData.split('\n')[3]
    return status


def synch(serviceTicket, peerIP=HOST):
    while checkStatus(serviceTicket, peerIP) != STATUS_READY:
        time.sleep(0.1)
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
    recoverMsg = serviceTicket+'\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(peerIP, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+recoverMsg)
    '''
    GET RESULTS
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    results = answerData.split('\n')[4]
    return results