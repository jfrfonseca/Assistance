import datetime, time
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer
from APIRequestAntenna import APIRequestAntenna
from cpnLibrary.implementation import AssistanceDBMS

        
        
        
class Transceiver():        
    log = ""
    
    
    def logEvent(self, logMessage):
        self.log += "\n"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" "+logMessage
        
             
    def __init__(self):
        self.log += "\n---------------- Assistance TRANSCEIVER service started up at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" ----------------\n"
        #set the program Antenna
        self.apiRequestAntenna = AssistanceSocketServer('', AssistanceDBMS.getPort('API_REQUEST'), APIRequestAntenna)
        
        
    def shutdown(self):
        self.apiRequestAntenna.shutdown()
        print "Transceiver is Off"

