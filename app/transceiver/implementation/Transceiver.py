import os, sys, ConfigParser, SocketServer
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '...'))
if not path in sys.path:
    sys.path.insert(1, path)
del path



class TransceiverProgramAntenna (SocketServer.StreamRequestHandler):
    # Settings ------------------------------------
    #General Settings
    #SETTINGS_FILE = ""
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
    
    
    def processData(self, receivedData):    
        processedData = str(receivedData).upper()
        return processedData
    
    
    def handle(self):
        #get settings
        if self.settingsParser == '' :
            self.settingsParser = ConfigParser.SafeConfigParser()
            self.settingsParser.read("../asssistanceTransceiverLocalSettingsFile.alsf")
            self.setSettings()
        #authentication
        authToken = self.rfile.readline().strip()
        if not self.authenticate(authToken, self.PROGRAM_TOKEN):
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")    
        #reading input data
        self.dataReceived = self.rfile.readline().strip()
        #processing the data
        self.data2send = self.processData(self.dataReceived)
        #writeback
        self.wfile.write(self.data2send)      
        
        
        
class Transceiver():                 
    def __init__(self):
        #get settings
        self.settingsParser = ConfigParser.SafeConfigParser()
        self.settingsParser.read("../asssistanceTransceiverLocalSettingsFile.alsf")
        #set the program Antenna
        self.PROGRAM_PORT = int(self.settingsParser.get("SERVER_PORTS", "PROGRAM_PORT"))
        self.programAntenna = AssistanceSocketServer('', self.PROGRAM_PORT, TransceiverProgramAntenna)
        
    def shutdown(self):
        self.programAntenna.shutdown()
        

    
