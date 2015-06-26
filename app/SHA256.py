#!/usr/bin/env python
'''
AssistanceApp class for the SHA256remoteTest, It will send a document over
a socket, perform it, and receive the results by socket
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
# ASSISTANCE MODULE IMPORTS ----------
from pkgTransceiver.AssistanceSockets\
    import AssistanceSocketClient
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import \
    TYPE_API_REQUEST_MSG, TYPE_DATA_SUBMIT_MSG, TYPE_STATUS_CHECK_MSG,\
    TYPE_RECOVER_RESULTS_MSG, PORT_API_REQUESTS, PORT_DATA_REQUESTS,\
    STATUS_GATHERING_DATA, STATUS_READY, SYMBOL_SEPARATOR,\
    TIME_DATA_SERVER_INTERVAL, AppID_SHA256_TEST, CHANNEL_FTP
# LOCAL CONSTANTS ----------------------------
HOST = '127.0.0.1'
# LAMBDA FUNCTIONS --------------------------
fileLength = lambda filePath: str(len(open(filePath, 'rb').read()))


def request(filePath, runTimes, peerIP=HOST, MYTOKEN="0123456789ABCDF"):
    '''
    Requests execution of the AssistanceApp.
Forms the message to be sent, specifying the parameters of the execution
of the app. Then, sends it and receives a ticket as answer
    :param filePath: the path to the file to be sent.
It will be used to determine the size of the file, necessary for the task submission.  # @IgnorePep8
    '''
    '''
    MAKE MSG
    '''
    header = MYTOKEN+'\n'+TYPE_API_REQUEST_MSG+'\n'
    apiRequestMsg = AppID_SHA256_TEST+'\n'\
        + runTimes + '\n'\
        + CHANNEL_FTP + '\n'\
        + fileLength(filePath) + '\n'\
        + CHANNEL_FTP + '\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(peerIP, PORT_API_REQUESTS)
    dummySocket.sendData(header+apiRequestMsg)
    '''
    GET TICKET
    '''
    answerData = dummySocket.receiveData()
    dummySocket.close()
    ticket = answerData.split('\n')[2]
    return ticket


def submit(serviceTicket, filePath, peerIP=HOST, MYTOKEN="0123456789ABCDF"):
    '''
    Sends a file over Assistance.
Waits until the task is ready to receive data, then sends it
    :param serviceTicket: the ticket of the task to be verified.
    :param filePath: The ABSPATH to the file to be sent.
    '''
    while checkStatus(serviceTicket, peerIP) != STATUS_GATHERING_DATA:
        time.sleep(TIME_DATA_SERVER_INTERVAL)
    dummySocket = AssistanceSocketClient(peerIP, PORT_DATA_REQUESTS)
    header = MYTOKEN + '\n' + TYPE_DATA_SUBMIT_MSG + '\n'
    submitMsg = serviceTicket+'\n'+filePath.split('/')[-1]+'\n'
    dummySocket.sendData(header + submitMsg)
    dummySocket.sendData(open(filePath, 'rb').read())
    dummySocket.close()


def checkStatus(serviceTicket, peerIP=HOST, MYTOKEN="0123456789ABCDF"):
    '''
    Sends a message checking the current status of the given ticket, and returns  # @IgnorePep8
        that status
    :param serviceTicket: the ticket of the task with the status is to be checked  # @IgnorePep8
    '''
    '''
    MAKE MSG
    '''
    header = MYTOKEN+'\n'+TYPE_STATUS_CHECK_MSG+'\n'
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


def synch(serviceTicket, peerIP=HOST, MYTOKEN="0123456789ABCDF"):
    '''
    Waits until the task is completed, and ready for redeem.
Then recovers the answers
    :param serviceTicket: ticket of the task to be recovered
    '''
    while checkStatus(serviceTicket, peerIP) != STATUS_READY:
        time.sleep(TIME_DATA_SERVER_INTERVAL)
    '''
    MAKE MSG
    '''
    header = MYTOKEN+'\n'+TYPE_RECOVER_RESULTS_MSG+'\n'
    recoverMsg = serviceTicket+'\n'
    '''
    SEND
    '''
    dummySocket = AssistanceSocketClient(peerIP, PORT_DATA_REQUESTS)
    dummySocket.sendData(header+recoverMsg)
    '''
    GET THE ANSWER FILES
    '''
    # creates the files to return
    stdout = "testsResults/"+serviceTicket+"-stdout.dat"
    stderr = "testsResults/"+serviceTicket+"-stderr.dat"
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
    # closes up and returns
    stdoutFile.close()
    stderrFile.close()
    dummySocket.close()
    return stdout, stderr
