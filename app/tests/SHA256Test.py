from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time
from cpnLibrary.implementation.Constants import *


ASSISTANCE_SERVER = '127.0.0.1'

#Sends the request to the API request server
def request():
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'\
                             +"60000 -verbose 20000"+'\n'\
                             +CHANNEL_LOCAL_FILE+'\n'\
                             +"/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat"+'\n'\
                             +CHANNEL_LOCAL_FILE+'\n'
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
    results = answerData.split('\n')[4] +'\n'+ answerData.split('\n')[5]
    return results

