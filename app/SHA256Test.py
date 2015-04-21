#!/usr/bin/env python
'''
AssistanceApp class for the SHA256Test, It will calculate the SHA256 of a local
file thousands of times and print the results
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
# ASSISTANCE MODULE IMPORTS ----------
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient  # @IgnorePep8
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import TOKEN_TESTS_VERSION,\
    AppID_SHA256_TEST, CHANNEL_LOCAL_FILE, PORT_API_REQUESTS, PORT_DATA_REQUESTS,\
    TYPE_STATUS_CHECK_MSG, TYPE_API_REQUEST_MSG, TYPE_RECOVER_RESULTS_MSG,\
    STATUS_READY
# LOCAL CONSTANTS ----------------------------
ASSISTANCE_SERVER = '127.0.0.1'


def request():
    '''
    Requests the run of the SHA256 over a local file, without data recovery
    '''
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'\
        + "60000 -verbose 20000" + '\n'\
        + CHANNEL_LOCAL_FILE + '\n'\
        + "testsData/experimentData.dat"+'\n'\
        + CHANNEL_LOCAL_FILE + '\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_API_REQUESTS)
    dummySocket.sendData(header+apiRequestMsg)
    '''
    GET TICKET
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    ticket = answerData.split('\n')[2]
    return ticket


def checkStatus(serviceTicket):
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
    statusCheckMsg = serviceTicket+'\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+statusCheckMsg)
    '''
    GET STATUS
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    status = answerData.split('\n')[3]
    return status


def synch(serviceTicket):
    '''
    Waits untill the task is completed, and ready for redeem
    '''
    while checkStatus(serviceTicket) != STATUS_READY:
        time.sleep(0.1)
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
    recoverMsg = serviceTicket+'\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+recoverMsg)
    '''
    GET RESULTS
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    results = answerData.split('\n')[4] + '\n'\
        + answerData.split('\n')[5]
    return results
