import time, SocketServer
from cpnLibrary.implementation import AssistanceDBMS
from pkgOfficer.implementation.Officer import TaskDescription


class DataAntenna (SocketServer.StreamRequestHandler):
    # INPUT Methods
    
    
    
    def authenticate(self, remoteToken):
        return remoteToken == AssistanceDBMS.getToken('API_REQUEST')
    
        
    def parseMessageType(self):
        # logTime
        timeReceived = time.time()
        # authentication token
        authToken = self.rfile.readline().strip()
        if not self.authenticate(authToken):
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")    
        # Assistance App Identification
        appID = self.rfile.readline().strip()
        # form of transference of the Assistance App Arguments (none, immediate, localFile, torrentFile)
        appArgsChannel = self.rfile.readline().strip()   
        # the AssistanceApp arguments (value for the method of getting arguments given above)
        appArgs = self.rfile.readline().strip()
        # form of transference of the Assistance App Data (none, immediate, localFile, torrentFile)
        appDataChannel = self.rfile.readline().strip()
        # the AssistanceApp data (value for the method of getting the data mentioned above)
        appDataDelivery = self.rfile.readline().strip()
        
        taskDescription = TaskDescription(authToken, timeReceived, appID, appArgsChannel, appArgs, appDataChannel, appDataDelivery)
        return taskDescription

    
    def handle(self):
        # parse the received data
        self.taskDescription = self.parseAssistanceRequest()
        # treats the data received and returns a service ticket
        taskTicket = self.getTicket()
        # print out some info
        print "Assistance APIRequest Server: received an AssistanceRequest\n\tfor AssistanceApp "+self.taskDescription.appID+";\n\tfrom API token "+self.taskDescription.authToken+";\n\ton port "+str(self.client_address[0])+";\n\tassigned Assistance ServiceTicket "+str(self.taskDescription.ticket)
        #writeback
        self.wfile.write(taskTicket)      
        
        