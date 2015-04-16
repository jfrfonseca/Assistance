import SocketServer
from cpnLibrary.implementation.Constants import *


class AssistanceGenericAntenna (SocketServer.StreamRequestHandler):
    localToken = ''
    
    def authenticate(self, remoteToken):
        
        #ONLY IN TESTS FVERSION
        self.localToken = TOKEN_TESTS_VERSION #ONLY IN TESTS VERSION
        
        if self.localToken == '':
            raise ValueError("Security Alert! Antenna has undefined authentication token!")
        if not remoteToken == self.localToken:
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")
    
    
    def parseMessageHeader(self):
        authToken = self.rfile.readline().strip()
        self.authenticate(authToken)
        msgType = self.rfile.readline().strip()
        return msgType, authToken

