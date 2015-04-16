import SocketServer, threading, socket, time
from cpnLibrary.implementation.AssistanceDBMS import TIME_SOCK_COOLDOWN,\
    DIR_APPS_CWD, SYMBOL_OK
from os.path import abspath
from cpnLibrary.implementation.Constants import TIME_DATA_SERVER_INTERVAL,\
    SYMBOL_SEPARATOR
  
#TODO implement this module with SSL
#Tutorials can be found in http://carlo-hamalainen.net/blog/2013/1/24/python-ssl-socket-echo-test-with-self-signed-certificate and https://devcenter.heroku.com/articles/ssl-certificate-self
class AssistanceSocketServer():
  
    def __init__(self, host, port, serverHandlerClass, serverArguments = []):   
        #define the variables
        self.HOST = host
        self.PORT = port

        # Create the server, binding to localhost on port 9999
        #self.serverObject = SocketServer.TCPServer((self.HOST, self.PORT), serverHandlerClass)
        self.serverObject = SocketServer.TCPServer((self.HOST, self.PORT), serverHandlerClass)
        self.serverObject.serverArguments = serverArguments
        self.serverThread = threading.Thread(target=self.serverObject.serve_forever)
        self.serverThread.start()
        #print "Server started"
        
    def shutdown(self):
        self.serverObject.shutdown()



class AssistanceSocketClient():
    
    bufferSize = 4096
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketObject.connect((self.host, self.port))
        
        
        
    def sendData(self, data):
        try:
            self.socketObject.sendall(data)
        finally:
            stall = 1
            
            
    def receiveData(self, bufsize=0):
        bufferSize = self.bufferSize
        if bufsize > 2:
            bufferSize = bufsize
        try:
            received = self.socketObject.recv(bufferSize)
        finally:
            return received
       
        
        
    def close(self):
        self.socketObject.close()
        time.sleep(TIME_SOCK_COOLDOWN)
        
        
        