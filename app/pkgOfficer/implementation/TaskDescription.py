'''
System Imports
'''
import datetime, threading, time

'''
Assistance Imports
'''
from cpnLibrary.implementation.Constants import *

       
class TaskDescription():
    def __init__(self, authToken, timeReceived, appID, appArgs, appDataChannel, appDataDelivery, appAnswerChannel):
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
        self.DATA_LOCATION = NULL
        
        # Task Answer Meta
        self.answer = {}
        self.STDOUT = NULL
        self.STDERR = NULL
        self.ANSWER_CHANNEL = appAnswerChannel
        self.OUTPUT_DIR = DIR_APPS_CWD+"outputs/"
        self.TIME_COMPLETED = NULL
        self.TIME_INTERRUPTED = NULL
        self.CHECKPOINT = NULL
        
        # Task Runtime Values
        self.SCRIPT = NULL
        self.workerThreads = {}
        self.lock = threading.Event()
        self.PROCESS_PRIORITY = NULL
    
        self.onlineLog = False
    
       
    def updateStatus(self, newStatus):
        appendString = "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Status update: ("+str(self.STATUS)+" --> "+str(newStatus)+");\n"
        self.LOG += appendString
        self.STATUS = newStatus
        self.seeLog()
        
        
        
    def changePriority(self, newPriority):
        self.LOG += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Changed Local processing priority from "+str(self.PROCESS_PRIORITY)+" to "+str(newPriority)+");\n"
        self.STATUS = newPriority
        self.seeLog()
        
        
    def logResourcesStatus(self, cpuMemDiskUsage):
        self.LOG += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- The current usage of system resources is: "
        self.LOG += "--free space (in AssistanceApps CWD partition): "+str(cpuMemDiskUsage["space"])+";\t"
        self.LOG += "--memory usage: "+str(cpuMemDiskUsage["memory"])+"%;\t"
        self.LOG += "--CPU usage: "+str(cpuMemDiskUsage["CPU"])+"%;\n"
        self.seeLog()
            
        
    def setTicket(self, ticketValue):
        if self.TICKET != NOT_APPLYED:
            raise ValueError("Security Alert! Attempt to overwrite Assistance ServiceTicket of task TICKET "+str(self.TICKET)+"!")
        else:
            self.TICKET = ticketValue
            self.LOG +=  "\t"+datetime.datetime.fromtimestamp(self.TIME_LABELED).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Assigned TICKET '"+str(self.TICKET)+"';\n"
            self.updateStatus(STATUS_WAITING)
        self.seeLog()
        
            
    def getResults(self):
        return self.answer
    
    def seeLog(self):
        if self.onlineLog:
            print >> open('LOG/0000_onlineLog.dat', 'a'), self.TICKET, "\t", self.LOG
    
    
        