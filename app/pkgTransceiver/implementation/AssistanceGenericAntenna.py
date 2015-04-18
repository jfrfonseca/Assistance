#!/usr/bin/env python
'''
Generic antenna that contains function to all other Assistance Antennas
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import SocketServer
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import TOKEN_TESTS_VERSION


class AssistanceGenericAntenna (SocketServer.StreamRequestHandler):
    '''
    Generic Antenna object with functions and basic requirements
    '''
    # TOKEN of the current instance of assistance
    localToken = ''

    def authenticate(self, remoteToken):
        '''
        Verifies authenticity of a token
        STUB method
        :param remoteToken: token received
        '''
        self.localToken = TOKEN_TESTS_VERSION
        if self.localToken == '':
            raise ValueError("Security Alert! Antenna has undefined authentication token!")  # @IgnorePep8
        if not remoteToken == self.localToken:
            raise ValueError("Security Alert! A client tried to connect to a Assistance Socket without the proper Authentication Token!")  # @IgnorePep8

    def parseMessageHeader(self):
        '''
        Parse the header of the message received,
        handles non-assistance messages, threats, etc
        '''
        authToken = self.rfile.readline().strip()
        self.authenticate(authToken)
        msgType = self.rfile.readline().strip()
        return msgType, authToken
