import time, datetime, threading, hashlib
import pkgMissionControl.implementation.Launcher, SystemStats
from cpnLibrary.implementation import AssistanceDBMS
from pkgPerformer.implementation import Performer
from cpnLibrary.implementation.Constants import *
from cpnLibrary.implementation.AssistanceDBMS import setTaskPriority
from pkgPerformer.implementation.Performer import interrupt


def includeNewTask(taskDescription):
    officerInstance = pkgMissionControl.implementation.Launcher.getOfficerInstance()
    #decides if there will be servicing to this request. If it does,
    if officerInstance.goNoGo(taskDescription):
        return officerInstance.includeTask(taskDescription)
    # if the request will NOT be serviced, returns a negative TICKET (literally). Default TICKET for "no go":-1
    else:
        return '-1'
       
        
        
class Officer():
    taskBuffer = {}
    
                    
    def generateTicket(self, taskDescription):
        #The TICKET must be the TIME_LABELED (time.time() defined here, 10.6 digits without punctuation), appended to the #TODO-signed SHA256 of the task's TIME_LABELED, localInstanceAuthToken, task's TOKEN, APPID, ARGUMENTS, DATA_DELIVERY
        tokenHash = hashlib.sha256()
        taskDescription.TIME_LABELED = time.time()
        
        tokenHash.update(str(taskDescription.TIME_LABELED))
        tokenHash.update(TOKEN_LOCAL)
        tokenHash.update(taskDescription.TOKEN)
        tokenHash.update(taskDescription.APPID)
        tokenHash.update(taskDescription.ARGUMENTS)
        tokenHash.update(taskDescription.DATA_DELIVERY)
        
        return str(taskDescription.TIME_LABELED).replace(".", "")+str(tokenHash.hexdigest())



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
        
        #checks the space(in Kb)  on the partition of the assistance working directory
        diskStatus = SystemStats.getFreeKbInAssistanceAppsCWD()
        
        #logs the current STATUS
        taskDescription.logResourcesStatus({"memory": memoryStatus, "CPU": CPUtotal, "space": SystemStats.getFreeSpaceInAssistanceAppsCWD_HumanReadable()})
        
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
        
        #Checks the disk usage in each partition, to only perform if there are enough space in the partition destined for the performer data and answer
        if diskStatus < thresholds["performLocal"]["disk"]["minimum"] or diskStatus > thresholds["performLocal"]["disk"]["maximum"]:
                distribution["local"]=False
        #if the disk usage is smaller than the minimum usage to perform remotely, or larger than the maximum, so it should not perform remotely
        if diskStatus < thresholds["performRemote"]["disk"]["minimum"] or diskStatus > thresholds["performRemote"]["disk"]["maximum"]:
                distribution["remote"]=False  
        
        #calculate performance priority of the task given the delta of the actual system usage to the ideal constraints
        setTaskPriority(taskDescription, CPUtotal, memoryStatus, diskStatus)
        
        return distribution



    def assignTask(self, task):
        remoteRun = False
        #launches the performers (local and remote) depending on the defined availability
        distributionOfExecution = self.defineDistribution(task)
        #the OR NOT is here to be sure that it will always run, even if only in one hemisphere!!
        #if it is to run locally
        if distributionOfExecution["local"] or not distributionOfExecution["remote"]:
            # if the task is ready
            if self.isReady2run(task):
                # starts the run locally
                Performer.perform(task)
        #if it is to run remotely
        if distributionOfExecution["remote"] or not distributionOfExecution["local"]:
            remoteRun = True
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().requestAssistance(task)
        # waits the first (remote or local) to complete
        task.lock.acquire()
        while task.TIME_COMPLETED == '':
            task.lock.wait()
        task.lock.release()
        # now one of the performers is done computing!
        #if the task was completed locally, cancels the remote one
        if task.STATUS == STATUS_COMPLETED_LOCAL or remoteRun:
            pkgMissionControl.implementation.Launcher.getTransceiverInstance().cancelRequest(task)
        #if it was completed, but not locally, cancels the local execution
        else:
            interrupt(task)
        #after completing the updates and interrupting unnecessary tasks, we update the result to READY
        task.updateStatus(STATUS_READY)
    
    
    def getTask(self, taskTicket):        
        return self.taskBuffer[taskTicket]
    
        
    def includeTask(self, newTask):
        newTask.setTicket(self.generateTicket(newTask))
        self.taskBuffer[newTask.TICKET] = newTask
        newTask = self.taskBuffer[newTask.TICKET]
        # starts the run process of the task
        newTask.workerThreads["director"] = threading.Thread(target=self.assignTask, args=(newTask, ))
        newTask.workerThreads["director"].start()
        return newTask.TICKET
    
    
    def getStatus(self, taskTicket):
        return self.getTask(taskTicket).STATUS               
       
    
    def goNoGo(self, taskDescription):
        # temporarily, a #STUB
        return True
        """
        if REJECTED:
        
        taskDescription.setTicket('-1')
        taskDescription.TIME_LABELED = time.time()
        AssistanceDBMS.logTask(taskDescription)
        """
    
    def isReady2run(self, task):
        if task.DATA_CHANNEL==NOT_APPLYED or task.DATA_CHANNEL==CHANNEL_LOCAL_FILE:
            return True
        elif task.DATA_CHANNEL==CHANNEL_FTP and not (self.getStatus(task.TICKET)==STATUS_WAITING or self.getStatus(task.TICKET)==STATUS_RECOVERING_DATA):
            return True
        return False
    
    
    # DevTools methods ----------------------------------------
    
    def printLogs(self):
        print "\n====================================\nLogs for all Assistance ServiceTickets in the Officer's Buffers as in "+datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S:%f')
        for ticket in self.taskBuffer.keys():
            print "ServiceTicket "+str(ticket)+" ("+self.getTask(ticket).STATUS+") Log:\n"+self.getTask(ticket).LOG
            
    def saveLogs(self):
        logTime = time.time()
        logFile = open(DIR_LOGS+str(int(time.time()))+".log", 'w')
        logFile.write("\n====================================\nLogs for all Assistance ServiceTickets in the Officer's Buffers as in "+datetime.datetime.fromtimestamp(logTime).strftime('%Y-%m-%d %H:%M:%S:%f'))
        for ticket in self.taskBuffer.keys():
            logFile.write("\nServiceTicket "+str(ticket)+" ("+self.getTask(ticket).STATUS+") Log:\n"+self.getTask(ticket).LOG)
        logFile.close()
            
            
            
        
        
