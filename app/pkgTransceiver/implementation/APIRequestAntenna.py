import time, SocketServer
from cpnLibrary.implementation import AssistanceDBMS
from pkgOfficer.implementation.Officer import TaskDescription, includeNewTask
import pkgMissionControl.implementation.Launcher


class APIRequestAntenna (SocketServer.StreamRequestHandler):
    def authenticate(self, remoteToken):
        return remoteToken == AssistanceDBMS.getToken('API_REQUEST')
    
    
    def parseMessageKind(self):
        # logTime
        timeReceived = time.time()
        # authentication token
        authToken = self.rfile.readline().strip()
        if not self.authenticate(authToken):
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")
        # Kind of the message: New request, or status check on already assigned Service Ticket
        msgKind = self.rfile.readline().strip()
        if not AssistanceDBMS.validMessageKind(msgKind):
            raise ValueError("Assistance APIRequest Server ERROR: Unknown Message Type!")
        return msgKind, authToken, timeReceived
            
        
        
    def parseAssistanceRequest(self, authToken, timeReceived):
        #if we are dealing with a new request message
        # Assistance App Identification
        appID = self.rfile.readline().strip()
        # the AssistanceApp arguments
        appArgs = self.rfile.readline().strip()
        # form of transference of the Assistance App Data (none, immediate, localFile, torrentFile)
        appDataChannel = self.rfile.readline().strip()
        # the AssistanceApp data (value for the method of getting the data mentioned above)
        appDataDelivery = self.rfile.readline().strip()
            
        taskDescription = TaskDescription(authToken, timeReceived, appID, appArgs, appDataChannel, appDataDelivery)
        return taskDescription
          
    
    def getTicket(self):    
        newTicket = includeNewTask(self.taskDescription)
        return newTicket
    
    
    
    
    def handle(self):
        # parse the received data
        msgKind, authToken, timeReceived = self.parseMessageKind()
        #check the kind of message we are dealing with, and deal accordingly
        #if it is a new request message:
        if msgKind == AssistanceDBMS.getSymbol("NEW_REQUEST", "MESSAGE_KIND"):
            self.taskDescription = self.parseAssistanceRequest(authToken, timeReceived)
            # treats the data received and returns a service ticket
            taskTicket = self.getTicket()
            # print out some info
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent("Assistance APIRequest Server: received an AssistanceRequest\n\tfor AssistanceApp "+self.taskDescription.appID+";\n\tfrom API token "+self.taskDescription.authToken+";\n\ton port "+str(self.client_address[0])+";\n\tassigned Assistance ServiceTicket "+str(self.taskDescription.ticket)+" ;")
            #writeback
            self.wfile.write(taskTicket)
        #if it is a status check message:
        elif msgKind == AssistanceDBMS.getSymbol("STATUS_CHECK", "MESSAGE_KIND"):
            #recover the already assigned Assistance ServiceTicket
            ticket2check = self.rfile.readline().strip()
            #gets the status of the task attached to the aforementioned ticket
            status = pkgMissionControl.implementation.Launcher.getOfficerInstance().getStatus(ticket2check)
            #logs this transaction
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().logEvent("Assistance APIRequest Server: received an AssistanceStatusCheck\n\tfrom API token "+authToken+";\n\ton port "+str(self.client_address[0])+";\n\tfor Assistance ServiceTicket "+str(ticket2check)+";\n\twhose status was: '"+status+"' ;")
            #writeback
            self.wfile.write(status)
            
            
            
            
            
            
        
        