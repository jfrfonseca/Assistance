import os, sys, time, ConfigParser, SocketServer
from pkgOfficer.implementation import Officer

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '...'))
if not path in sys.path:
    sys.path.insert(1, path)
del path



class APIRequestAntenna (SocketServer.StreamRequestHandler):
    # Settings ------------------------------------
    #General Settings
    #SETTINGS_FILE = ""
    MAX_MESSAGE_LINES = 16
    # Server Ports
    #PROGRAM_PORT = -1
    #PORTAL_PORT = -1
    # Client Ports
    #LIBRARY_PORT = -1
    # Server Tokens
    PROGRAM_TOKEN = ''
    #PORTAL_TOKEN = ''
    # Client Tokens
    #LIBRARY_TOKEN = ''
    
    # Objects ------------------------------------
    settingsParser = ''

   
    def setSettings(self):
        # Server Ports
        #self.PROGRAM_PORT = int(self.settingsParser.get("SERVER_PORTS", "PROGRAM_PORT"))
        #self.PORTAL_PORT = int(self.settingsParser.get("SERVER_PORTS", "PORTAL_PORT"))
        # Client Ports
        #self.LIBRARY_PORT = int(self.settingsParser.get("CLIENT_PORTS", "LIBRARY_PORT"))
        # Server Tokens
        self.PROGRAM_TOKEN = self.settingsParser.get("SERVER_TOKENS", "PROGRAM_TOKEN")
        #self.PORTAL_TOKEN = self.settingsParser.get("SERVER_TOKENS", "PORTAL_TOKEN")
        # Client Tokens
        #self.LIBRARY_TOKEN = self.settingsParser.get("CLIENT_TOKENS", "LIBRARY_TOKEN")
       
            
    def authenticate(self, remoteToken, localToken):
        return remoteToken == localToken
    
        
    def parseAssistanceRequest(self):
        # logTime
        timeReceived = time.time()
        # authentication token
        authToken = self.rfile.readline().strip()
        if not self.authenticate(authToken, self.PROGRAM_TOKEN):
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")    
        # Assistance App Identification
        assistanceAppID = self.rfile.readline().strip()
        # form of transference of the Assistance App Arguments (none, immediate, localFile, FTP, torrentMagnetLink, torrentFile)
        assistanceAppArgumentsChannel = self.rfile.readline().strip()
        # the AssistanceApp arguments (value for the method of getting arguments given above)
        assistanceAppArgumentsRoute = self.rfile.readline().strip()
        # form of transference of the Assistance App Data (none, immediate, localFile, FTP, torrentMagnetLink, torrentFile)
        assistanceAppDataChannel = self.rfile.readline().strip()
        # the AssistanceApp data (value for the method of getting the data mentioned above)
        assistanceAppDataRoute = self.rfile.readline().strip()
        
        taskDescription = [timeReceived, authToken, assistanceAppID, assistanceAppArgumentsChannel, assistanceAppArgumentsRoute, assistanceAppDataChannel, assistanceAppDataRoute]
        return taskDescription
          
    
    def getTicket(self):    
        taskDescription = self.parseAssistanceRequest()
        newTicket = Officer.includeNewTask(taskDescription)
        return newTicket
    
    
    def handle(self):
        #get settings
        if self.settingsParser == '' :
            self.settingsParser = ConfigParser.SafeConfigParser()
            self.settingsParser.read("../asssistanceTransceiverLocalSettingsFile.alsf")
            self.setSettings()
        # treats the data received and returns a service ticket
        taskTicket = self.getTicket()
        #writeback
        self.wfile.write(taskTicket)      
        
        
        
        