import SocketServer
from cpnLibrary.implementation import AssistanceDBMS
from cpnLibrary.implementation.AssistanceDBMS import TYPE_API_REQUEST_MSG,\
    TYPE_STATUS_CHECK_MSG


class AssistanceGenericAntenna (SocketServer.StreamRequestHandler):
    localToken = ''
    
    def authenticate(self, remoteToken):
        if self.localToken == '':
            raise ValueError("Security Alert! Antenna has undefined authentication token!")
        return remoteToken == self.localToken
    
    
    def makeAnswerHeader(self, answerType, taskTicket):
        header = self.localToken+"\n"
        header += answerType+"\n"
        header += taskTicket+"\n"
        return header
    
    
    def parseMessageHeader(self):
        # authentication token
        authToken = self.rfile.readline().strip()
        if not self.authenticate(authToken):
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")
        # Kind of the message: New request, or status check on already assigned Service Ticket
        msgKind = self.rfile.readline().strip()
        #if not msgKind in [TYPE_API_REQUEST_MSG, TYPE_STATUS_CHECK_MSG]:
            #raise ValueError("Assistance APIRequest Server ERROR: Unknown Message Type!")
        return msgKind, authToken

