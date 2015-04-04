from cpnLibrary.implementation.AssistanceDBMS import TOKEN_TRANSCEIVER_TEST,\
    TYPE_API_REQUEST_MSG, AppID_LOCAL_ECHO_TEST, NOT_APPLYED, PORT_API_REQUESTS
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time

def request(messageToEcho):
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_LOCAL_ECHO_TEST+'\n'+messageToEcho+'\n'+NOT_APPLYED+'\n'+NOT_APPLYED+'\n'
    dummySocket = AssistanceSocketClient('', PORT_API_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+apiRequestMsg)
    #print "receiving ticket"
    time.sleep(0.1)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[2]