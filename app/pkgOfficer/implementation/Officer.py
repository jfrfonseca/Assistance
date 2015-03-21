from random import Random
from cpnLibrary.implementation import AssistanceDBMS


def includeNewTask(taskDescription):
    return "0123"



class TaskDescription():

    def getHash(self):
        return '0123456789ABCDEF'
 
    def __init__(self, authToken, timeReceived, origin, appID, appArgsChannel, appArgs, appDataChannel, appDataDelivery, appAnswerChannel, appAnswerDelivery):
        #Task General Meta
        self.ticket = AssistanceDBMS.getSymbol('NONE')
        self.status = AssistanceDBMS.getSymbol('DRAFT', ['STATUS'])
            # Task Orign Data
        self.authToken = authToken
        self.timeReceived = timeReceived
        self.origin = origin
        
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
        
        