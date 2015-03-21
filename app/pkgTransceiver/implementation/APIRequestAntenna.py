import time, SocketServer
from cpnLibrary.implementation import AssistanceDBMS
from pkgOfficer.implementation.Officer import TaskDescription, includeNewTask


class APIRequestAntenna (SocketServer.StreamRequestHandler):
    def authenticate(self, remoteToken):
        return remoteToken == AssistanceDBMS.getToken('API_REQUEST')
    
        
    def parseAssistanceRequest(self):
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
        # form of transference of the Assistance App Answer (none, immediate, localFile, torrentFile)
        appAnswerChannel = self.rfile.readline().strip()
        #  the AssistanceApp Answer delivery data (immediate, localFile, torrentFile)
        appAnswerDelivery = self.rfile.readline().strip()
        
        taskDescription = TaskDescription(authToken, timeReceived, AssistanceDBMS.getSymbol("LOCALHOST"), appID, appArgsChannel, appArgs, appDataChannel, appDataDelivery, appAnswerChannel, appAnswerDelivery)
        return taskDescription
          
    
    def getTicket(self):    
        taskDescription = self.parseAssistanceRequest()
        newTicket = includeNewTask(taskDescription)
        return newTicket
    
    
    def handle(self):
        # treats the data received and returns a service ticket
        taskTicket = self.getTicket()
        #writeback
        self.wfile.write(taskTicket)      
        
        
        
        