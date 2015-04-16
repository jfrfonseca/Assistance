import time, datetime, threading, hashlib
import pkgMissionControl.implementation.Launcher, SystemStats
from cpnLibrary.implementation import AssistanceDBMS
from pkgPerformer.implementation import Performer
from cpnLibrary.implementation.AssistanceDBMS import getTaskPriority
from pkgPerformer.implementation.Performer import interrupt
from random import randint
from pkgOfficer.implementation.TaskDescription import TaskDescription
from cpnLibrary.implementation.Constants import STATUS_WAITING, STATUS_REJECTED,\
    TOKEN_TESTS_VERSION, NULL, STATUS_GATHERING_DATA, DIR_LOGS, CHANNEL_FTP,\
    STATUS_PERFORMING_LOCAL, STATUS_STANDBY, STATUS_SETTING_UP,\
    CHANNEL_LOCAL_FILE, DIR_APPS_CWD, STATUS_READY, STATUS_DATA_READY
import cpnLibrary.implementation.AssistanceDBMS
import os.path

       
class Officer():
    '''
    BUFFER THAT CONTAINS ALL THE NON-FINISHED TASKS
    '''
    taskBuffer = {}
    
    '''
    Includes a new task to the buffer, and decides if will access the task or not  it or not
    '''
    def include(self, taskDescription):
        ticket = self.generateTicket(taskDescription)
        self.taskBuffer[ticket] = taskDescription
        taskDescription.TICKET = ticket
        if self.decide(ticket):
            taskDescription.updateStatus(STATUS_WAITING)
            #creates a thread to manage the running of the task
            taskDescription.workerThreads["director"] = threading.Thread(target=self.setup, args=(ticket, ))
            taskDescription.workerThreads["director"].start()
            #returns the ticket
            return ticket
        else:
            taskDescription.updateStatus(STATUS_REJECTED)
            #TODO add task to dead archive
            return NULL
    
    '''
    Generates a new ServiceTicket to the most recent task received and processed
    '''
    def generateTicket(self, taskDescription):
        #The TICKET must be the TIME_LABELED (time.time() defined here, 10.6 digits without punctuation), appended to 4 random digits,  appended to the #TODO-signed SHA256 of the task's TIME_LABELED, localInstanceAuthToken, task's TOKEN, APPID, ARGUMENTS, DATA_DELIVERY
        tokenHash = hashlib.sha256()
        taskDescription.TIME_LABELED = time.time()
        
        tokenHash.update(str(taskDescription.TIME_LABELED))
        tokenHash.update(TOKEN_TESTS_VERSION)
        tokenHash.update(taskDescription.TOKEN)
        tokenHash.update(taskDescription.APPID)
        tokenHash.update(taskDescription.ARGUMENTS)
        tokenHash.update(taskDescription.DATA_DELIVERY)
        
        #the 4 random digits below are here to avoid that two equal tasks from the same source at the same time do not share a ticket!
        randomQuartet = str(randint(0, 9999))
        while len(randomQuartet) < 4:
            randomQuartet = '0'+randomQuartet
        
        return str(taskDescription.TIME_LABELED).replace(".", "")+randomQuartet+str(tokenHash.hexdigest())

    
    '''
    GETTER TO THE TASK BUFFER
    '''
    def getTask(self, ticket):
        if ticket in self.taskBuffer.keys():
            return self.taskBuffer[ticket]
        else:
            #TODO check the dead archive
            return TaskDescription(NULL, NULL, NULL, NULL, NULL, NULL, NULL)
    
    '''
    Decides if this instance will attend to the task or not
    TESTS VERSION
    '''
    def decide(self, ticket):
        return True


    def enoughLocalResources(self, ticket):
        locallyAvailable = True
        #gets the task that are being wirked with
        task = self.getTask(ticket)
        #gets the thrasholds of system limits for the current task to be performed
        thresholds = AssistanceDBMS.getThresholds(task)
        #Checks the current usage of Memory
        memoryStatus = SystemStats.getMemoryUsage()
        #checks the TOTAL current usage of CPU
        CPUstatus = SystemStats.getCPUusage()
        CPUtotal = 0
        for index in range(len(CPUstatus)):
            CPUtotal += CPUstatus[index]
        CPUtotal /= len(CPUstatus)
        #checks the space(in Kb)  on the partition of the assistance working directory
        diskStatus = SystemStats.getFreeKbInAssistanceAppsCWD()
        #logs the current status of the system
        task.logResourcesStatus({"memory": memoryStatus, "CPU": CPUtotal, "space": SystemStats.getFreeSpaceInAssistanceAppsCWD_HumanReadable()})
        #if the CPU usage is smaller than the minimum usage to perform locally, or larger than the maximum, so it should not perform locally
        if CPUtotal < thresholds["performLocal"]["CPU"]["minimum"] or CPUtotal > thresholds["performLocal"]["CPU"]["maximum"]:
            locallyAvailable=False
        #if the memory usage is smaller than the minimum usage to perform locally, or larger than the maximum, so it should not perform locally    
        for memoryKind in memoryStatus.keys():
            if memoryStatus[memoryKind] < thresholds["performLocal"]["memory"]["minimum"][memoryKind] or memoryStatus[memoryKind] > thresholds["performLocal"]["memory"]["maximum"][memoryKind]:
                locallyAvailable=False
        #if there is too much or too little space, does not perform locally 
        if diskStatus < thresholds["performLocal"]["disk"]["minimum"] or diskStatus > thresholds["performLocal"]["disk"]["maximum"]:
                locallyAvailable=False
        #calculate performance priority of the task given the delta of the actual system usage to the ideal constraints
        task.PROCESS_PRIORITY = AssistanceDBMS.getTaskPriority(task, CPUtotal, memoryStatus, diskStatus)
        #returns the availability of the current machine to this task
        return locallyAvailable
                    
                    
    def setup(self, ticket):
        task = self.getTask(ticket)
        #if it will perform locally
        if self.enoughLocalResources(ticket):
            task.updateStatus(STATUS_GATHERING_DATA) ########## GATHERING THE TASK DATA
            #if the data file is already on the local machine, the data location will be the relative directory to the assistance CWD
            if task.DATA_CHANNEL == CHANNEL_LOCAL_FILE:
                task.DATA_LOCATION = os.path.relpath(task.DATA_DELIVERY, os.getcwd())
                task.updateStatus(STATUS_DATA_READY)
            #if the data file is not on the local machine, it expects it will be in the data folder of the Apps CWD
            elif task.DATA_CHANNEL == CHANNEL_FTP:
                task.DATA_LOCATION = DIR_APPS_CWD+'data/'
                task.lock.wait()
                task.lock.clear()
            else:
                task.updateStatus(STATUS_DATA_READY)
            ##################################### MAKING THE TASK READY TO EXECUTE
            task.SCRIPT = cpnLibrary.implementation.AssistanceDBMS.getCallerScript(task)
            task.updateStatus(STATUS_STANDBY) ############### TASK IS READY TO BE RUN
            Performer.perform(task)
        #if it will be performed remotelly
        #TODO request remote assistance
        
        
        ######################################## WAITS FOR THE TASK TO BE COMPLETED, REMOTE OR LOCALLY!
        task.lock.wait()
        task.updateStatus(STATUS_READY)

    '''

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
            else:
                break
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
        elif task.DATA_CHANNEL==CHANNEL_FTP:
            return False
        return False
    
    '''
    
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

            
            
        
        
