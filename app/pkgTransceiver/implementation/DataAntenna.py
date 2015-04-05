import SocketServer, time
from cpnLibrary.implementation import AssistanceDBMS
from pkgOfficer.implementation.Officer import TaskDescription
import pkgMissionControl.implementation.Launcher
from pkgTransceiver.implementation.AssistanceGenericAntenna import AssistanceGenericAntenna
from cpnLibrary.implementation.AssistanceDBMS import TYPE_STATUS_CHECK_MSG,\
    TYPE_STATUS_CHECK_ANS, TOKEN_TRANSCEIVER_TEST, TYPE_RECOVER_RESULTS_MSG,\
    STATUS_COMPLETED_LOCAL, STATUS_COMPLETED_REMOTE, TYPE_RECOVER_RESULTS_ANS,\
    STATUS_READY


class DataAntenna (AssistanceGenericAntenna):    
    
    def handle(self):
        
        self.localToken = TOKEN_TRANSCEIVER_TEST
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
            status = pkgMissionControl.implementation.Launcher.getOfficerInstance().getStatus(ticket2check)+'\n'
            #logs this transaction
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent("Assistance DataTransfer Server: received an AssistanceStatusCheck message\n\tfrom API token "+authToken+";\n\ton port "+str(self.client_address[0])+";\n\tat: "+str(timeReceived)+";\n\tfor Assistance ServiceTicket "+str(ticket2check)+";\n\twhose status was: '"+status+"' ;")
            #writeback
            self.wfile.write(self.makeAnswerHeader(TYPE_STATUS_CHECK_ANS, ticket2check)+status)
           
        #if it is a message demanding the results    
        elif msgType == TYPE_RECOVER_RESULTS_MSG:
            #recover the already assigned Assistance ServiceTicket
            ticket2check = self.rfile.readline().strip()
            #gets the status of the task attached to the aforementioned ticket
            status = pkgMissionControl.implementation.Launcher.getOfficerInstance().getStatus(ticket2check)+'\n'
            #logs this transaction
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent("Assistance DataTransfer Server: received an Assistance RecoverResults message\n\tfrom API token "+authToken+";\n\ton port "+str(self.client_address[0])+";\n\tat: "+str(timeReceived)+";\n\tfor Assistance ServiceTicket "+str(ticket2check)+";\n\twhose status was: '"+status+"' ;")
            #writeback
            if status == STATUS_READY+'\n':
                channel, output, errors = AssistanceDBMS.normalizeOutput( pkgMissionControl.implementation.Launcher.getOfficerInstance().getTask(ticket2check))
                self.wfile.write(self.makeAnswerHeader(TYPE_RECOVER_RESULTS_ANS, ticket2check)+channel+'\n\t'+output+'\n\t'+errors+'\n')
            else:
                self.wfile.write(self.makeAnswerHeader(TYPE_STATUS_CHECK_ANS, ticket2check)+status)
        else:
            errorString = "Assistance DataTransfer Server ERROR: Message of the wrong type sent to Assistance DataTransfer Server!\tMessage Type received: '"+msgType+"'\tMessageTypes Accepted: '"+TYPE_STATUS_CHECK_MSG+"'\n"
            self.wfile.write(errorString)
            raise ValueError(errorString)
        
        