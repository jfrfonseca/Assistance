#!/usr/bin/env python
'''
Module to create and run sockets specially designed for Assistance
The Client one is non-preemptive, the Server is on a new Thread
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import SocketServer
import threading
import socket
from cpnLibrary.implementation.Constants import SYMBOL_SEPARATOR


class AssistanceSocketServer():
    '''
    Threaded socket that waits for connections, and must be initiated with
    a handler class
    #TODO implement this module with SSL
    Tutorials in:
http://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate
https://devcenter.heroku.com/articles/ssl-certificate-self
    '''

    def __init__(self, port, serverHandlerClass, serverArguments=[]):
        '''
        Initiates the Socket Server Thread and sets it to run until closed
        Runs in Localhost always
        :param port: Port to the SocketServer to be run on
        :param serverHandlerClass: Class that handles the connections to the socket  # @IgnorePep8
        :param serverArguments: Arguments to be passed to the Handler Class
        '''
        self.PORT = port
        self.serverObject = SocketServer.TCPServer(
            ('', self.PORT), serverHandlerClass)
        self.serverObject.serverArguments = serverArguments
        self.serverThread = threading.Thread(
            target=self.serverObject.serve_forever)
        self.serverThread.start()

    def shutdown(self):
        '''
        Shuts down this socket's thread, finishing its execution immediately
        Should be called every time a socket will no longer be used
        '''
        self.serverObject.shutdown()


class AssistanceSocketClient():
    '''
    Socket Client. Simplifies using sockets to transport data and files
    '''
    # Buffer to download data over the sockets
    bufferSize = 4096

    def __init__(self, host, port):
        '''
        Creates the socket connected to another
        :param host: IP of the partner server socket
        :param port: Port the partner Server is running the socket server
        '''
        self.host = host
        self.port = port
        self.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketObject.connect((self.host, self.port))

    def sendData(self, data):
        '''
        Sends some data over the socket. Must be heard with a sock.recv() wild
        :param data: The data to be sent as buffer or string
        '''
        try:
            self.socketObject.sendall(data)
        finally:
            stall = 1

    def receiveData(self, bufsize=0):
        '''
        Receives some data over the socket.
        :param bufsize: size of the buffer to keep the data in in each iteration.  Minimal is 2 # @IgnorePep8
        '''
        bufferSize = self.bufferSize
        if bufsize > 2:
            bufferSize = bufsize
        try:
            received = self.socketObject.recv(bufferSize)
        finally:
            return received

    '''def receiveFile(self, fileName):
        with open(fileName, 'wb') as fileReceived:
            while True:
                received = self.socketObject.recv(self.bufferSize)
                while (received):
                    if received.endswith(SYMBOL_SEPARATOR):
                        str2write = received[:-len(SYMBOL_SEPARATOR)]
                        fileReceived.write(str2write)
                        break
                    else:
                        fileReceived.write(received)
                        received = self.socketObject.recv(self.bufferSize)
                break'''

    def sendFile(self, fileName):
        while True:
            with open(fileName, 'rb') as file2send:
                while 1:
                    fileData = file2send.read()
                    if fileData == '':
                        break
                    self.socketObject.sendall(fileData)
            # self.socketObject.sendall(SYMBOL_SEPARATOR)
            break

    def close(self):
        '''
        Closes the socket
        '''
        self.socketObject.close()
