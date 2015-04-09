from pkgOfficer.implementation.TaskDescription import TaskDescription
import pkgMissionControl.implementation.Launcher, time
from pkgTransceiver.implementation.AssistanceGenericAntenna import AssistanceGenericAntenna
from cpnLibrary.implementation.Constants import *
from pkgOfficer.implementation.Officer import includeNewTask


class APIRequestAntenna (AssistanceGenericAntenna):
  
        
    def parseAssistanceRequest(self, authToken, timeReceived):
        #if we are dealing with a new request message
        # Assistance App Identification
        appID = self.rfile.readline().strip()
        # the AssistanceApp arguments
        appArgs = self.rfile.readline().strip()
        #print "parsed APPID and args"
        # form of transference of the Assistance App Data (none, immediate, localFile, torrentFile)
        appDataChannel = self.rfile.readline().strip()
        #print "parsed data channel"
        # the AssistanceApp data (value for the method of getting the data mentioned above)
        appDataDelivery = self.rfile.readline().strip()
        #print "parsed data meta"
            
        taskDescription = TaskDescription(authToken, timeReceived, appID, appArgs, appDataChannel, appDataDelivery)
        return taskDescription
          
    
    def getTicket(self):    
        newTicket = includeNewTask(self.taskDescription)
        return newTicket
    
    
    def handle(self):
        #print "received message"
        self.localToken = TOKEN_LOCAL
        # logTime
        timeReceived = time.time()
        # parse the received data header
        msgKind, authToken = self.parseMessageHeader()
        #print "header parsed"
        #check the kind of message we are dealing with, and deal accordingly
        #if it is a new request message:
        if msgKind == TYPE_API_REQUEST_MSG:
            #print "parsing request"
            self.taskDescription = self.parseAssistanceRequest(authToken, timeReceived)
            #print "request parsed"
            # treats the data received and returns a service TICKET
            taskTicket = self.getTicket()
            #print "got TICKET"
            # print out some info
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent("Assistance APIRequest Server: received an AssistanceRequest\n\tfor AssistanceApp "+self.taskDescription.APPID+";\n\tfrom API token "+self.taskDescription.TOKEN+";\n\ton port "+str(self.client_address[0])+";\n\tassigned Assistance ServiceTicket "+str(self.taskDescription.TICKET)+" ;")
            #writeback the answer header and the time of arrival of the message
            #print "sending answer"
            self.wfile.write(self.makeAnswerHeader(TYPE_API_REQUEST_ANS, taskTicket)+str(timeReceived)+"\n")
        # if it is not a New Request Message:
        else:
            errorString = "Assistance APIRequest Server ERROR: Message of the wrong type sent to Assistance APIRequest Server!\tMessage Type received: '"+msgKind+"'\tMessageTypes Accepted: '"+TYPE_API_REQUEST_MSG+"'\n"
            self.wfile.write(errorString)
            raise ValueError(errorString)
            
            
            
            
            
            
        
        