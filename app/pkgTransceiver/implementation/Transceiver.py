import datetime, time, os
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
        
        
    def requestAssistance(self, taskDescription):
        #STUB
        stall = 1
        
        
    def cancelRequest(self, taskDescription):
        #STUB
        stall = 1
        
        
        
        
        
        
        
