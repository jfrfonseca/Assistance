import os, sys, ConfigParser
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer
from APIRequestAntenna import APIRequestAntenna

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '...'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
        
        
        
class Transceiver():                 
    def __init__(self):
        #get settings
        self.settingsParser = ConfigParser.SafeConfigParser()
        self.settingsParser.read("../asssistanceTransceiverLocalSettingsFile.alsf")
        #set the program Antenna
        self.PROGRAM_PORT = int(self.settingsParser.get("SERVER_PORTS", "PROGRAM_PORT"))
        self.programAntenna = AssistanceSocketServer('', self.PROGRAM_PORT, APIRequestAntenna)
        
    def shutdown(self):
        self.programAntenna.shutdown()
        print "Transceiver is Off"
        

    
