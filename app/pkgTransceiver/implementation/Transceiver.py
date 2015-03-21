from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer
from APIRequestAntenna import APIRequestAntenna
from cpnLibrary.implementation import AssistanceDBMS

        
        
        
class Transceiver():                 
    def __init__(self):
        #set the program Antenna
        self.apiRequestAntenna = AssistanceSocketServer('', AssistanceDBMS.getPort('API_REQUEST'), APIRequestAntenna)
        
    def shutdown(self):
        self.apiRequestAntenna.shutdown()
        print "Transceiver is Off"
        

    
