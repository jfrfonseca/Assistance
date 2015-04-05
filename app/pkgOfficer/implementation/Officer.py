import time, datetime, threading
import pkgMissionControl.implementation.Launcher, SystemStats
from cpnLibrary.implementation import AssistanceDBMS
from pkgPerformer.implementation import Performer
from cpnLibrary.implementation.AssistanceDBMS import NOT_APPLYED, STATUS_DRAFT,\
    STATUS_WAITING


def includeNewTask(taskDescription):
    officerInstance = pkgMissionControl.implementation.Launcher.getOfficerInstance()
    ticket = officerInstance.includeTask(taskDescription)
    return ticket



class TaskDescription():
    def __init__(self, authToken, timeReceived, appID, appArgs, appDataChannel, appDataDelivery):
        #Task General Meta
        self.ticket = NOT_APPLYED
        self.status = STATUS_DRAFT
        self.log = "\t"+datetime.datetime.fromtimestamp(timeReceived).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- New task (appID '"+str(appID)+"') received by Assistance from token "+authToken+";\n"
        self.authToken = authToken
        self.timeReceived = timeReceived
        
        # Task Request Meta
        self.appID = appID
        self.dataChannel = appDataChannel
        # Task Request Data
        self.appArgs = appArgs
        self.dataDelivery = appDataDelivery
        self.gatheredDataLocation = ''
        
        # Task Answer Meta
        self.answer = {}
        self.timeCompleted = ''
        self.timeInterrupted = ''
        self.checkpoint = ''
        
        # Task Runtime Values
        self.callerScript = ''
        self.workerThreads = {}
        self.lock = threading.Condition()
        self.localProcessPriority = 10
    
    
       
    def updateStatus(self, newStatus):
        self.log += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Status update: ("+str(self.status)+" --> "+str(newStatus)+");\n"
        self.status = newStatus
        
        
    def changePriority(self, newPriority):
        self.log += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Changed Local processing priority from "+str(self.localProcessPriority)+" to "+str(newPriority)+");\n"
        self.status = newPriority
        
        
    def logResourcesStatus(self, cpuMemUsage):
        self.log += "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- The current usage of system resources is: "
        for resourceName in cpuMemUsage.keys():
            self.log += "--"+str(resourceName)+": "+str(cpuMemUsage[resourceName])+" %; "
        self.log += "\n"
            
        
    def setTicket(self, ticketValue):
        if self.ticket != NOT_APPLYED:
            raise ValueError("Security Alert! Attempt to overwrite Assistance ServiceTicket of task ticket "+str(self.ticket)+"!")
        else:
            self.ticket = ticketValue
            self.log +=  "\t"+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')+" |- Assigned ticket '"+str(self.ticket)+"';\n"
            self.updateStatus(STATUS_WAITING)
        
            
    def getResults(self):
        return self.answer
        
        
        
class Officer():
    taskBuffer = {}
    testTicket = 0
    
                    
    def generateTicket(self, taskDescription):
        #TODO Make it more robust and coherent
        self.testTicket += 1
        return "testTicket"+str(self.testTicket)


    def defineDistribution(self, taskDescription):
        distribution = {"local": True, "remote":True}
        #checks if there are enough resources so it is reasonable to request remote assistance. the SystemStats module provides this information
        
        #Gets the minimal usage needed to request assistance remotely
        thresholds = AssistanceDBMS.getThresholds(taskDescription, request=True)
        
        #Checks the usage of Memory
        memoryStatus = SystemStats.getMemoryUsage()
        
        #checks the TOTAL usage of CPU
        CPUstatus = SystemStats.getCPUusage()
        CPUtotal = 0
        for index in range(len(CPUstatus)):
            CPUtotal += CPUstatus[index]
        CPUtotal /= len(CPUstatus)
        
        taskDescription.logResourcesStatus({"memory": memoryStatus, "CPU (average)": CPUtotal})
        
        #decides if there should be a local and a remote execution of this task. Maybe there should always be a local
        #if the CPU usage is smaller than the minimum usage to perform locally, or larger than the maximum, so it should not perform locally
        if CPUtotal < thresholds["performLocal"]["CPU"]["minimum"] or CPUtotal > thresholds["performLocal"]["CPU"]["maximum"]:
            distribution["local"]=False
        #if the CPU usage is smaller than the minimum usage to perform remotely, or larger than the maximum, so it should not perform remotely
        if CPUtotal < thresholds["performRemote"]["CPU"]["minimum"] or CPUtotal > thresholds["performRemote"]["CPU"]["maximum"]:
            distribution["remote"]=False
            
        #decides to see if there will be a local or remote performance of the task. Maybe there should be ALWAYS a local performance
        for memoryKind in memoryStatus.keys():
            #if the memory usage is smaller than the minimum usage to perform locally, or larger than the maximum, so it should not perform locally
            if memoryStatus[memoryKind] < thresholds["performLocal"]["memory"]["minimum"][memoryKind] or memoryStatus[memoryKind] > thresholds["performLocal"]["memory"]["maximum"][memoryKind]:
                distribution["local"]=False
            #if the memory usage is smaller than the minimum usage to perform remotely, or larger than the maximum, so it should not perform remotely
            if memoryStatus[memoryKind] < thresholds["performRemote"]["memory"]["minimum"][memoryKind] or memoryStatus[memoryKind] > thresholds["performRemote"]["memory"]["maximum"][memoryKind]:
                distribution["remote"]=False  
        
        #TODO Checks the disk usage in each partition, to only perform if there are enough space in the partition destined for the performer data and answer
        #TODO calculate performance priority given the delta of the actual system usage to the ideal constraints
        
        return distribution


    def assignTask(self, task):
        #TODO implement the call for remote execution, the interrupt f the still not ready execution, the check for availability
        #launches the performers (local and remote) depending on the defined availability
        distributionOfExecution = self.defineDistribution(task)
        #the OR NOT is here to be sure that it will always run, even if only in one hemisphere!!
        #if it is to run locally
        if distributionOfExecution["local"] or not distributionOfExecution["remote"]:
            # starts the run locally
            Performer.perform(task)
        #if it is to run remotely
        if distributionOfExecution["remote"] or not distributionOfExecution["local"]:
            #TODO requests assistance from remote peer
            #this is a "nop" operation
            nop = 1
        # waits the first (remote or local) to complete
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
    
    
    def getStatus(self, taskTicket):
        return self.getTask(taskTicket).status               
       
    
    # DevTools methods ----------------------------------------
    
    def printLogs(self):
        print "\n====================================\nLogs for all Assistance ServiceTickets in the Officer's Buffers:"
        for ticket in self.taskBuffer.keys():
            print "ServiceTicket "+str(ticket)+" ("+self.getTask(ticket).status+") Log:\n"+self.getTask(ticket).log
        
        
