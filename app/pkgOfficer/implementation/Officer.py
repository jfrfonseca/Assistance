from cpnLibrary.implementation import AssistanceDBMS
import pkgMissionControl.implementation.Launcher
import random


def includeNewTask(taskDescription):
    officerInstance = pkgMissionControl.implementation.Launcher.getOfficerInstance()
    ticket = officerInstance.includeTask(taskDescription)
    return ticket



class TaskDescription(): 
    def __init__(self, authToken, timeReceived, appID, appArgsChannel, appArgs, appDataChannel, appDataDelivery, appAnswerChannel, appAnswerDelivery):
        #Task General Meta
        self.ticket = AssistanceDBMS.getSymbol('NONE')
        self.status = AssistanceDBMS.getSymbol('DRAFT', 'STATUS')
        self.log="- Received by Assistance in "+str(timeReceived)+";\n"
        self.authToken = authToken
        
        # Task Request Meta
        self.appID = appID
        self.argsChannel = appArgsChannel
        self.dataChannel = appDataChannel
            # Task Request Data
        self.args = appArgs
        self.dataDelivery = appDataDelivery
        
        # Task Answer Meta
        self.answerChannel = appAnswerChannel
        self.answerDelivery = appAnswerDelivery
        
        
    def updateStatus(self, newStatus):
        self.status = newStatus
        
        
    def setTicket(self, ticketValue):
        if self.ticket != AssistanceDBMS.getSymbol('NONE'):
            raise ValueError("Security Alert! Attempt to overwrite Assistance ServiceTicket of task ticket "+str(self.ticket)+"!")
        else:
            self.ticket = ticketValue
        
        
        
class Officer():
    taskBuffer = {}
    testTicket = 0
    assignerThread = ''
    
    
#    def assignTask(self):
#        # get a task from the buffer
#        random.choice(self.taskBuffer.keys())
#        if 
        
        
        
        
    def generateTicket(self, taskDescription):
        self.testTicket += 1
        return "testTicket"+str(self.testTicket)
    
        
    def includeTask(self, newTask):
        newTask.setTicket(self.generateTicket(newTask))
        self.taskBuffer[newTask.ticket] = newTask
        return self.getTask(newTask.ticket).ticket
    
    
    def getTask(self, taskTicket):
        return self.taskBuffer[taskTicket]
    
    
    def printTaskBuffer(self):
        print "All Assistance ServiceTickets in the Officer's Tasks Buffer:"
        for ticket in self.taskBuffer.keys():
            print "\t"+str(ticket)
        
        