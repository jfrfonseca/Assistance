import SocketServer, threading, socket
  

class AssistanceSocketServer():
    
  
    def __init__(self, host, port, serverHandlerClass):   
        #define the variables
        self.HOST = host
        self.PORT = port

        # Create the server, binding to localhost on port 9999
        #self.serverObject = SocketServer.TCPServer((self.HOST, self.PORT), serverHandlerClass)
        self.serverObject = SocketServer.TCPServer((self.HOST, self.PORT), serverHandlerClass)
        self.serverThread = threading.Thread(target=self.serverObject.serve_forever)
        self.serverThread.start()
        #print "Server started"
        
    def shutdown(self):
        self.serverObject.shutdown()



class AssistanceSocketClient():
    
    def __init__(self, host, port, authToken):
        self.host = host
        self.port = port
        self.authToken = authToken
        self.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def sendData(self, data):
        try:
            # Connect to server and send data
            self.socketObject.connect((self.host, self.port))
            self.socketObject.sendall(self.authToken + "\n"+ data + "\n")
        finally:
            #print "Data sent to "+str(self.host)+":"+str(self.port)
            stall = 1
            
    def receiveData(self):
        try:
            received = self.socketObject.recv(1024)
        finally:
            #print "Data received thought port "+str(self.port)
            return received
        
    def close(self):
        self.socketObject.close()






    
    

class AssistanceEchoServer(SocketServer.StreamRequestHandler):

    REQUIRED_TOKEN = "0123456789ABCDEF"
    
    def authenticate(self):
        return self.authToken == self.REQUIRED_TOKEN
    
    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.authToken = self.rfile.readline().strip()
        
        if not self.authenticate():
            raise ValueError("Security Alert! A client tryed to connect to a Assistance Socket without the proper Authentication Token!")    
        
        self.data = self.rfile.readline().strip()
        
        #print ("Server received a message!\nToken "+self.authToken+" wrote:")
        #print (self.data)
        
        print "processing the data"
        
        self.data = str(self.data).upper()
        
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data)

if __name__ == "__main__":
    host = 'localhost'
    port = 23019
    token = "0123456789ABCDEF"
    message = "It worked."
    
    print "Running a Sockets Echo Test on "+host+":"+str(port)
    
    #server = AssistanceSocketServer(host, port, AssistanceEchoServer)
    server = AssistanceSocketServer(host, port, AssistanceEchoServer)
    client = AssistanceSocketClient(host, port, token)
    print "Sockets are up. Sending message\n"
    client.sendData(message)
    print "Message sent. Receiving message\n"
    receivedString = client.receiveData()
    print receivedString
    
    client.close()
    server.shutdown()
    
    
    
    
    