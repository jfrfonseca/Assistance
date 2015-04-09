from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time
from cpnLibrary.implementation.Constants import *


ASSISTANCE_SERVER = '127.0.0.1'

#Sends the request to the API request server
def request():
    header = TOKEN_LOCAL+'\n'\
                 +TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'\
                             +"60000 -verbose 20000"+'\n'\
                             +CHANNEL_LOCAL_FILE+'\n'+\
                             "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat"+'\n'
    #Create the socket to submit the AssistanceRequest
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_API_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+apiRequestMsg)
    #print "receiving ticket"
    time.sleep(TIME_SOCK_COOLDOWN)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[2]


def checkStatus(serviceTicket):
    header = TOKEN_LOCAL+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
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
        header = TOKEN_LOCAL+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
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
