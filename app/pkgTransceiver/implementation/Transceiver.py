import datetime, time, os.path
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer
from pkgTransceiver.implementation.APIRequestAntenna import APIRequestAntenna
from pkgTransceiver.implementation.DataAntenna import DataAntenna
from cpnLibrary.implementation.Constants import *

        
        
        
class Transceiver():        
    LOG = ""
    
    
    def logEvent(self, logMessage):
        self.LOG += "\n"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" "+logMessage
        
             
    def __init__(self):
        self.LOG += "\n---------------- Assistance TRANSCEIVER service started up at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" ----------------\n"
        #set the API requests Antenna
        self.apiRequestAntenna = AssistanceSocketServer('', PORT_API_REQUESTS, APIRequestAntenna)
        #set the Data  Antenna
        self.dataAntenna = AssistanceSocketServer('', PORT_DATA_REQUESTS, DataAntenna)
        
        
    def shutdown(self):
        self.apiRequestAntenna.shutdown()
        self.dataAntenna.shutdown()
        print "Transceiver is Off"


    def gatherData(self, taskDescription):
        #if there is no data to be passed
        if taskDescription.DATA_CHANNEL == NOT_APPLYED:
            return ''
        #if the data file is already on the local machine
        elif taskDescription.DATA_CHANNEL == CHANNEL_LOCAL_FILE:
            return os.path.relpath(taskDescription.DATA_DELIVERY, os.getcwd())
        else:
            return NOT_APPLYED
        
        
    def requestAssistance(self, taskDescription):
        #STUB
        stall = 1
        
        
    def cancelRequest(self, taskDescription):
        #STUB
        stall = 1
        
        
        
        
        
        
        
