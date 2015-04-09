'''
System Imports
'''
import datetime, threading, time

'''
Assistance Imports
'''
from cpnLibrary.implementation.Constants import *

       
class TaskDescription():
    def __init__(self, authToken, timeReceived, appID, appArgs, appDataChannel, appDataDelivery):
        #Task General Meta
        self.TICKET = NOT_APPLYED
        self.STATUS = STATUS_DRAFT
        self.LOG = "\t"+datetime.datetime.fromtimestamp(timeReceived).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- New task (APPID '"+str(appID)+"') received by Assistance from token "+authToken+";\n"
        self.TOKEN = authToken
        self.TIME_RECEIVED = timeReceived
        self.TIME_LABELED = NOT_APPLYED
        
        # Task Request Meta
        self.APPID = appID
        self.DATA_CHANNEL = appDataChannel
        # Task Request Data
        self.ARGUMENTS = appArgs
        self.DATA_DELIVERY = appDataDelivery
        self.DATA_LOCATION = ''
        
        # Task Answer Meta
        self.answer = {}
        self.STDOUT = ''
        self.STDERR = ''
        self.ANSWER_CHANNEL = ''
        self.OUTPUT_DIR = ''
        self.TIME_COMPLETED = ''
        self.TIME_INTERRUPTED = ''
        self.CHECKPOINT = ''
        
        # Task Runtime Values
        self.SCRIPT = ''
        self.workerThreads = {}
        self.lock = threading.Condition()
        self.PROCESS_PRIORITY = TUNNING_DEFAULT_PROCESS_PRIORITY
    
    
       
    def updateStatus(self, newStatus):
        self.LOG += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Status update: ("+str(self.STATUS)+" --> "+str(newStatus)+");\n"
        self.STATUS = newStatus
        
        
    def changePriority(self, newPriority):
        self.LOG += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Changed Local processing priority from "+str(self.PROCESS_PRIORITY)+" to "+str(newPriority)+");\n"
        self.STATUS = newPriority
        
        
    def logResourcesStatus(self, cpuMemDiskUsage):
        self.LOG += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- The current usage of system resources is: "
        self.LOG += "--free space (in AssistanceApps CWD partition): "+str(cpuMemDiskUsage["space"])+";\t"
        self.LOG += "--memory usage: "+str(cpuMemDiskUsage["memory"])+"%;\t"
        self.LOG += "--CPU usage: "+str(cpuMemDiskUsage["CPU"])+"%;\n"
            
        
    def setTicket(self, ticketValue):
        if self.TICKET != NOT_APPLYED:
            raise ValueError("Security Alert! Attempt to overwrite Assistance ServiceTicket of task TICKET "+str(self.TICKET)+"!")
        else:
            self.TICKET = ticketValue
            self.LOG +=  "\t"+datetime.datetime.fromtimestamp(self.TIME_LABELED).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Assigned TICKET '"+str(self.TICKET)+"';\n"
            self.updateStatus(STATUS_WAITING)
        
            
    def getResults(self):
        return self.answer
        