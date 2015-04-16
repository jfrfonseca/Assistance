from pkgOfficer.implementation.TaskDescription import TaskDescription
import pkgMissionControl.implementation.Launcher, time
from pkgTransceiver.implementation.AssistanceGenericAntenna import AssistanceGenericAntenna
from cpnLibrary.implementation.Constants import TYPE_API_REQUEST_ANS,\
    TYPE_API_REQUEST_MSG


getTicket = lambda task : pkgMissionControl.implementation.Launcher.getOfficerInstance().include(task)

class APIRequestAntenna (AssistanceGenericAntenna):
  
  
    def parseAssistanceRequest(self, authToken, timeReceived):
        appID = self.rfile.readline().strip()
        appArgs = self.rfile.readline().strip()
        appDataChannel = self.rfile.readline().strip()
        appDataDelivery = self.rfile.readline().strip()
        appAnswerChannel = self.rfile.readline().strip()
        task = TaskDescription(authToken, timeReceived, appID, appArgs, appDataChannel, appDataDelivery, appAnswerChannel)
        return task
             
    
    def handle(self):
        timeReceived = time.time()
        msgType, authToken = self.parseMessageHeader()
        if msgType == TYPE_API_REQUEST_MSG:
            task = self.parseAssistanceRequest(authToken, timeReceived)
            ticket = getTicket(task)
            self.wfile.write(self.localToken+"\n"+TYPE_API_REQUEST_ANS+"\n" + ticket+"\n")
        else:
            errorString = "Assistance APIRequest Server ERROR: Message of the wrong type sent to Assistance APIRequest Server!\tMessage Type received: '"+msgType
            self.wfile.write(errorString)
            raise ValueError(errorString)
            
            
            
            
            
            
        
        