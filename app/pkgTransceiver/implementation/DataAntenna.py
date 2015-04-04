import SocketServer
from cpnLibrary.implementation import AssistanceDBMS
from pkgOfficer.implementation.Officer import TaskDescription
import pkgMissionControl.implementation.Launcher
from pkgTransceiver.implementation.AssistanceGenericAntenna import AssistanceGenericAntenna


class DataAntenna (AssistanceGenericAntenna):    
    
    def handle(self):
        # parse the received data
        msgKind, authToken, timeReceived = self.parseMessageHeader('DATA')
        #check the kind of message we are dealing with, and deal accordingly
        #if it is a new request message:
        if msgKind == AssistanceDBMS.getSymbol("STATUS_CHECK", "MESSAGE_KIND"):
            #recover the already assigned Assistance ServiceTicket
            ticket2check = self.rfile.readline().strip()
            #gets the status of the task attached to the aforementioned ticket
            status = pkgMissionControl.implementation.Launcher.getOfficerInstance().getStatus(ticket2check)
            #logs this transaction
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent("Assistance APIRequest Server: received an AssistanceStatusCheck\n\tfrom API token "+authToken+";\n\ton port "+str(self.client_address[0])+";\n\tat: "+str(timeReceived)+";\n\tfor Assistance ServiceTicket "+str(ticket2check)+";\n\twhose status was: '"+status+"' ;")
            #writeback
            self.wfile.write(self.getAnswerHeader(ticket2check)+status)
        else:
            errorString = "Assistance APIRequest Server ERROR: Message of the wrong type sent to Assistance APIRequest Server!\tMessage Type received: '"+msgKind+"'\tMessageTypes Accepted: '"+AssistanceDBMS.getSymbol("NEW_REQUEST", "MESSAGE_KIND")+"'\n"
            self.wfile.write(errorString)
            raise ValueError(errorString)
        
        