from threading import Thread
from WebSocketServer import WebSocketServer  # @UnresolvedImport

def socketThread(socketObject):
    socketObject.serveforever()


class WebSocketThreadObject():
    def __init__(self, host, port):
        self.port = port
        self.host = host
        self.socketObject = WebSocketServer(self.host, self.port)
        self.socketActiveThread = Thread(target = socketThread, args = (self.socketObject,))
        self.socketActiveThread.start()
    
    def getMessagesBuffer(self):
        data = self.socketObject.getMessageBuffer()
        if len(data) < 1:
            data = ['']
        return data
    
    def clearMessagesBuffer(self):
        self.socketObject.clearMessageBuffer()
        
    def sendMessage(self, message):
        self.socketObject.sendMessage(message)
        
       
    



