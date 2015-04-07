from cpnLibrary.implementation.AssistanceDBMS import TOKEN_TRANSCEIVER_TEST,\
    TYPE_API_REQUEST_MSG, NOT_APPLYED, PORT_API_REQUESTS,\
    AppID_SHA256_TEST, CHANNEL_LOCAL_FILE, TYPE_STATUS_CHECK_MSG, PORT_DATA_REQUESTS,\
    TYPE_RECOVER_RESULTS_MSG, STATUS_READY, TYPE_RECOVER_RESULTS_ANS,\
    CHANNEL_FTP
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time

ASSISTANCE_SERVER = '127.0.0.1'

def request():
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'+"60000 -verbose 20000"+'\n'+CHANNEL_FTP+'\n'+"TODO THE DATA FILE"+'\n'
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_API_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+apiRequestMsg)
    #print "receiving ticket"
    time.sleep(0.1)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[2]


def checkStatus(serviceTicket):
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
    statusCheckMsg = serviceTicket+'\n'
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+statusCheckMsg)
    #print "receiving ticket"
    time.sleep(0.1)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[3]


def downloadData():
    output = answerData.split('\n')[4]
    errors = answerData.split('\n')[5]


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
    return answerData.split('\n')[4] +'\n'+ answerData.split('\n')[5]