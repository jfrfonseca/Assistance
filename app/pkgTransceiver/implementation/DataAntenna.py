import time
from pkgTransceiver.implementation.AssistanceGenericAntenna import AssistanceGenericAntenna
from cpnLibrary.implementation.Constants import *
from pkgPerformer.implementation import Performer
from cpnLibrary.implementation.AssistanceDBMS import *
import pkgMissionControl.implementation.Launcher


class DataAntenna (AssistanceGenericAntenna):
    
    def handle(self):    
        
                                                
        getTask = lambda ticket: pkgMissionControl.implementation.Launcher.getOfficerInstance().getTask(ticket)
    
        transceiverLOG = lambda message, token, timeReceived, ticket, status:\
                                                pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent(\
                                                            message+token\
                                                            +";\n\ton port "+str(self.client_address[0])\
                                                            +";\n\tat: "+str(timeReceived)\
                                                            +";\n\tfor Assistance ServiceTicket "+str(ticket)\
                                                            +";\n\twhose status was: '"+status+"' ;")    
                                                
        self.localToken = TOKEN_TESTS_VERSION
        
        timeReceived = time.time()
        msgType, authToken = self.parseMessageHeader()
        #check the kind of message we are dealing with, and deal accordingly
        #handles the message to check the status
        if msgType == TYPE_STATUS_CHECK_MSG:
            ticket2check = self.rfile.readline().strip()
            task = getTask(ticket2check)     
            transceiverLOG("Assistance DataTransfer Server: received an AssistanceStatusCheck message\n\tfrom API token ", authToken, timeReceived, ticket2check, task.STATUS)
            self.wfile.write(self.localToken+'\n'+TYPE_RECOVER_RESULTS_ANS+'\n'+ticket2check+'\n'+task.STATUS+'\n')
            
        #handle the message to recover the results    
        elif msgType == TYPE_RECOVER_RESULTS_MSG:
            ticket2check = self.rfile.readline().strip()
            task = getTask(ticket2check)     
            transceiverLOG("Assistance DataTransfer Server: received an Assistance RecoverResults message\n\tfrom API token ", authToken, timeReceived, ticket2check, task.STATUS)
            while task.STATUS != STATUS_READY:
                task = getTask(ticket2check)     
                time.sleep(TIME_DATA_SERVER_INTERVAL)          
            #outputs the data of the task
            if task.ANSWER_CHANNEL == CHANNEL_FTP:
                stdoutFile = open(task.STDOUT, 'rb')
                stderrFile = open(task.STDERR, 'rb')
                stdout = stdoutFile.read()
                stderr = stderrFile.read()
                task.updateStatus(STATUS_SENDING_DATA)
                self.request.sendall(stdout)
                self.request.sendall(SYMBOL_SEPARATOR)
                self.request.sendall(stderr)
                task.updateStatus(STATUS_FINISHED)
                stdoutFile.close()
                stderrFile.close()
            else:
                self.wfile.write(self.localToken+'\n'+TYPE_RECOVER_RESULTS_ANS+'\n'+ticket2check+'\n'\
                                 +CHANNEL_IMMEDIATE+'\n'+task.STDOUT+'\n'+task.STDERR+'\n')
                            
        #if this is a message to submit a file
        elif msgType == TYPE_DATA_SUBMIT_MSG:
            ticket = self.rfile.readline().strip()
            task = getTask(ticket)
            while task.STATUS != STATUS_GATHERING_DATA:
                task = getTask(ticket2check)     
                time.sleep(TIME_DATA_SERVER_INTERVAL)
            #recovers the file name to be saved, and its size
            fileName = self.rfile.readline().strip()
            fileSize = int(task.DATA_DELIVERY)
            task.DATA_LOCATION= task.DATA_LOCATION+fileName
            #recovers the data of the file, and saves it to a file
            recoveredData = self.request.recv(fileSize)
            dataFile = open(task.DATA_LOCATION, 'wb')
            dataFile.write(recoveredData)
            dataFile.close()
            #updates the task data location and status, and unlocks the task's setup thread
            task.updateStatus(STATUS_DATA_READY)
            task.lock.set()            
        
        else:
            errorString = "Assistance DataTransfer Server ERROR: Message of the wrong type sent to Assistance DataTransfer Server!\tMessage Type received: '"+msgType+'\n'
            self.wfile.write(errorString)
            raise ValueError(errorString)
        
        