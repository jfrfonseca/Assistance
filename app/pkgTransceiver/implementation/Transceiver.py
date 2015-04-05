import datetime, time
import os.path
from pkgTransceiver.implementation.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer
from pkgTransceiver.implementation.APIRequestAntenna import APIRequestAntenna
from pkgTransceiver.implementation.DataAntenna import DataAntenna
from cpnLibrary.implementation.AssistanceDBMS import PORT_API_REQUESTS,\
    NOT_APPLYED, CHANNEL_LOCAL_FILE, PORT_DATA

        
        
        
class Transceiver():        
    log = ""
    
    
    def logEvent(self, logMessage):
        self.log += "\n"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" "+logMessage
        
             
    def __init__(self):
        self.log += "\n---------------- Assistance TRANSCEIVER service started up at "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" ----------------\n"
        #set the API requests Antenna
        self.apiRequestAntenna = AssistanceSocketServer('', PORT_API_REQUESTS, APIRequestAntenna)
        #set the Data  Antenna
        self.dataAntenna = AssistanceSocketServer('', PORT_DATA, DataAntenna)
        
        
    def shutdown(self):
        self.apiRequestAntenna.shutdown()
        self.dataAntenna.shutdown()
        print "Transceiver is Off"


    def gatherData(self, taskDescription):
        #if there is no data to be passed
        if taskDescription.dataChannel == NOT_APPLYED:
            return ''
        #if the data file is already on the local machine
        elif taskDescription.dataChannel == CHANNEL_LOCAL_FILE:
            return os.path.relpath(taskDescription.dataDelivery, os.getcwd())
        else:
            return NOT_APPLYED
        
        
        
        
        
        
        
