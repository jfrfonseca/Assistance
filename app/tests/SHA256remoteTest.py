from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient
import time
import os
from cpnLibrary.implementation.Constants import *

ASSISTANCE_SERVER = '127.0.0.1'

fileLength = lambda filePath : str(len(open(filePath, 'rb').read()))

def request(filePath):
    '''
    MAKE MSG
    '''
    header = TOKEN_TESTS_VERSION+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'\
                             +"60000 -verbose 20000"+'\n'\
                             +CHANNEL_FTP+'\n'\
                             +fileLength(filePath)+'\n'\
                             +CHANNEL_FTP+'\n'
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



def submit(serviceTicket, filePath):
    while checkStatus(serviceTicket) != STATUS_GATHERING_DATA:
        time.sleep(TIME_DATA_SERVER_INTERVAL)
    dummySocket = AssistanceSocketClient(ASSISTANCE_SERVER, PORT_DATA_REQUESTS)
    header = TOKEN_TESTS_VERSION + '\n' + TYPE_DATA_SUBMIT_MSG + '\n'
    submitMsg = serviceTicket+'\n'
    dummySocket.sendData(header + submitMsg)
    dummySocket.sendData(open(filePath, 'rb').read())
    dummySocket.close()



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
        time.sleep(TIME_DATA_SERVER_INTERVAL)
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
    GET THE ANSWER FILES
    '''
    #creates the files to return
    stdout = "tests/"+serviceTicket+"-stdout.dat"
    stderr = "tests/"+serviceTicket+"-stderr.dat"
    stdoutFile = open(stdout, 'wb')
    stderrFile = open(stderr, 'wb')
    currentFile = stdoutFile
    receivedData = dummySocket.receiveData()
    while receivedData:
        if SYMBOL_SEPARATOR in receivedData:
            filePieces = receivedData.split(SYMBOL_SEPARATOR)
            stdoutFile.write(filePieces[0])
            stderrFile.write(filePieces[1])
            currentFile = stderrFile
        else:
            currentFile.write(receivedData)
        receivedData = dummySocket.receiveData()
    #closes up and returns
    stdoutFile.close()
    stderrFile.close()
    dummySocket.close()
    return stdout+'\n'+stderr


