from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time
import os
from cpnLibrary.implementation.Constants import *

ASSISTANCE_SERVER = '127.0.0.1'

def request(dataFile):
    fileLength = str(os.stat(dataFile).st_size)
    header = TOKEN_LOCAL+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'+"60000 -verbose 20000"+'\n'+CHANNEL_FTP+'\n'+fileLength+'\n'
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_API_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+apiRequestMsg)
    #print "receiving ticket"
    time.sleep(TIME_SOCK_COOLDOWN)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[2]


def submit(serviceTicket, fileName):
    header = TOKEN_LOCAL+'\n'+TYPE_DATA_SUBMIT_MSG+'\n'
    dataSubmitMsg = serviceTicket+'\n'
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+dataSubmitMsg)
    dummySocket.sendFile(os.path.abspath("tests/test0data.dat"), fileName)
    dummySocket.close()


def recover(serviceTicket):
    header = TOKEN_LOCAL+'\n'+TYPE_DATA_RECOVER_MSG+'\n'
    dataRecoverMsg = serviceTicket+'\n'
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+dataRecoverMsg)
    output = dummySocket.receiveFile(os.getcwd())
    errors = dummySocket.receiveFile(os.getcwd())
    dummySocket.close()
    return output, errors


def checkStatus(serviceTicket):
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
    statusCheckMsg = serviceTicket+'\n'
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+statusCheckMsg)
    #print "receiving ticket"
    time.sleep(TIME_SOCK_COOLDOWN)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[3]



def synchronise(serviceTicket):
    msgType = ""
    while not msgType == TYPE_RECOVER_RESULTS_ANS:
        header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
        recoverMsg = serviceTicket+'\n'
        dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
        #print "sending message"
        dummySocket.sendData(header+recoverMsg)
        #print "receiving ticket"
        answerData = dummySocket.receiveData()
        #print "closing socket"
        dummySocket.close()
        msgType = answerData.split('\n')[1]
    outputPath, errorsPath = recover(serviceTicket)
    return outputPath, errorsPath