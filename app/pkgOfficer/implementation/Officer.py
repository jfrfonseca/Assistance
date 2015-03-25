from cpnLibrary.implementation import AssistanceDBMS
import pkgMissionControl.implementation.Launcher
import random, time, datetime, threading
from pkgPerformer.implementation import Performer


def includeNewTask(taskDescription):
    officerInstance = pkgMissionControl.implementation.Launcher.getOfficerInstance()
    ticket = officerInstance.includeTask(taskDescription)
    return ticket



class TaskDescription():
    def __init__(self, authToken, timeReceived, appID, appArgsChannel, appArgs, appDataChannel, appDataDelivery):
        #Task General Meta
        self.ticket = AssistanceDBMS.getSymbol('NONE')
        self.status = AssistanceDBMS.getSymbol('DRAFT', 'STATUS')
        self.log = "\t"+datetime.datetime.fromtimestamp(timeReceived).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- New task (appID '"+str(appID)+"') received by Assistance from token "+authToken+";\n"
        self.authToken = authToken
        self.timeReceived = timeReceived
        
        # Task Request Meta
        self.appID = appID
        self.argsChannel = appArgsChannel
        self.dataChannel = appDataChannel
            # Task Request Data
        self.args = appArgs
        self.dataDelivery = appDataDelivery
        
        # Task Answer Meta
        self.answer = {}
        self.timeCompleted = ''
        self.timeInterrupted = ''
        self.checkpoint = ''
        
        # Task Runtime Values
        self.callerScript = ''
        self.workerThreads = {}
        self.lock = threading.Condition()
        
        
    def updateStatus(self, newStatus):
        self.log += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Status update: ("+str(self.status)+" --> "+str(newStatus)+");\n"
        self.status = newStatus
        
        
    def setTicket(self, ticketValue):
        if self.ticket != AssistanceDBMS.getSymbol('NONE'):
            raise ValueError("Security Alert! Attempt to overwrite Assistance ServiceTicket of task ticket "+str(self.ticket)+"!")
        else:
            self.ticket = ticketValue
            self.log +=  "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Assigned ticket '"+str(self.ticket)+"';\n"
            self.updateStatus(AssistanceDBMS.getSymbol('WAITING', 'STATUS'))
            
        
        
        
        
class Officer():
    taskBuffer = {}
    testTicket = 0
    
                    
    def generateTicket(self, taskDescription):
        self.testTicket += 1
        return "testTicket"+str(self.testTicket)


    def assignTask(self, task):
        # starts the run locally
        Performer.perform(task)
        # check if there is local availability for the chosen task. if not, requests Assistance from a peer
        #if not localAvailability(chosenTask):
        # requests assistance from remote TODO
        # waits the first to complete
        task.lock.acquire()
        while task.timeCompleted == '':
            task.lock.wait()
            # IF THE REMOTE finishes first, interrupts the local. if the local finishes first, sends an interrupt for the remote. the remote can also send a checkpoint, and the local must import this checkpoint TODO
        # now one of the performers is done computing!
        task.lock.release()
    
    
    def getTask(self, taskTicket):        
        return self.taskBuffer[taskTicket]
    
        
    def includeTask(self, newTask):
        newTask.setTicket(self.generateTicket(newTask))
        self.taskBuffer[newTask.ticket] = newTask
        newTask = self.taskBuffer[newTask.ticket]
        # starts the run process of the task
        newTask.workerThreads["director"] = threading.Thread(target=self.assignTask, args=(newTask, ))
        newTask.workerThreads["director"].start()
        
        return newTask.ticket
                
       
    
    # DevTools methods ----------------------------------------
    
    def printLogs(self):
        print "\n====================================\nLogs for all Assistance ServiceTickets in the Officer's Buffers:"
        for ticket in self.taskBuffer.keys():
            print "ServiceTicket "+str(ticket)+" ("+self.getTask(ticket).status+") Log:\n"+self.getTask(ticket).log
        
        
