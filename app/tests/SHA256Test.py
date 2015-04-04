from cpnLibrary.implementation.AssistanceDBMS import TOKEN_TRANSCEIVER_TEST,\
    TYPE_API_REQUEST_MSG, NOT_APPLYED, PORT_API_REQUESTS,\
    AppID_SHA256_TEST, CHANNEL_LOCAL_FILE
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time

def request():
    header = TOKEN_TRANSCEIVER_TEST+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'+NOT_APPLYED+'\n'+CHANNEL_LOCAL_FILE+'\n'+"/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat"+'\n'
    dummySocket = AssistanceSocketClient('', PORT_API_REQUESTS)
    #print "sending message"
    dummySocket.sendData(header+apiRequestMsg)
    #print "receiving ticket"
    time.sleep(0.1)
    answerData = dummySocket.receiveData()
    #print "closing socket"
    dummySocket.close()
    return answerData.split('\n')[2]