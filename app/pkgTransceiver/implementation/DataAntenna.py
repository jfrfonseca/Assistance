import time
from pkgTransceiver.implementation.AssistanceGenericAntenna import AssistanceGenericAntenna
from cpnLibrary.implementation.Constants import *
from pkgPerformer.implementation import Performer
from cpnLibrary.implementation.AssistanceDBMS import *
import pkgMissionControl.implementation.Launcher


class DataAntenna (AssistanceGenericAntenna):
    
    def handle(self):    
            
        getStatus = lambda ticket:\
                                                pkgMissionControl.implementation.Launcher.getOfficerInstance().getStatus(ticket)
    
        transceiverLOG = lambda message, token, timeReceived, ticket, status:\
                                                pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent(\
                                                            message+token\
                                                            +";\n\ton port "+str(self.client_address[0])\
                                                            +";\n\tat: "+str(timeReceived)\
                                                            +";\n\tfor Assistance ServiceTicket "+str(ticket)\
                                                            +";\n\twhose status was: '"+status+"' ;")    
                                                
        getTask = lambda ticket: pkgMissionControl.implementation.Launcher.getOfficerInstance().getTask(ticket)
                                                
        self.localToken = TOKEN_LOCAL
        # logTime
        timeReceived = time.time()
        # parse the received data
        msgType, authToken = self.parseMessageHeader()
        #check the kind of message we are dealing with, and deal accordingly
        #if it is a new request message:
        
        if msgType == TYPE_STATUS_CHECK_MSG:
            #recover the already assigned Assistance ServiceTicket
            ticket2check = self.rfile.readline().strip()
            #gets the status of the task attached to the aforementioned ticket
            status = getStatus(ticket2check)+'\n'
            #logs this transaction
            transceiverLOG("Assistance DataTransfer Server: received an AssistanceStatusCheck message\n\tfrom API token ", authToken, timeReceived, ticket2check, status)
            #writeback
            self.wfile.write(self.makeAnswerHeader(TYPE_STATUS_CHECK_ANS, ticket2check)+status)
            
        #if it is a message demanding the results    
        elif msgType == TYPE_RECOVER_RESULTS_MSG:
            #recover the already assigned Assistance ServiceTicket
            ticket2check = self.rfile.readline().strip()
            #gets the status of the task attached to the aforementioned ticket
            status = getStatus(ticket2check)+'\n'
            #logs this transaction
            
            transceiverLOG("Assistance DataTransfer Server: received an Assistance RecoverResults message\n\tfrom API token ", authToken, timeReceived, ticket2check, status)
            #writeback
            if status == STATUS_READY+'\n':
                channel, output, errors = normalizeOutput(getTask(ticket2check))
                self.wfile.write(self.makeAnswerHeader(TYPE_RECOVER_RESULTS_ANS, ticket2check)+channel+'\n\t'+output+'\n\t'+errors+'\n')
            else:
                self.wfile.write(self.makeAnswerHeader(TYPE_STATUS_CHECK_ANS, ticket2check)+status)
            
        
        else:
            errorString = "Assistance DataTransfer Server ERROR: Message of the wrong type sent to Assistance DataTransfer Server!\tMessage Type received: '"+msgType+'\n'
            self.wfile.write(errorString)
            raise ValueError(errorString)
        
        