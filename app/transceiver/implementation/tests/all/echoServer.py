import signal, sys
from threading import Thread
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer  # @UnresolvedImport

class SimpleEcho(WebSocket):
    def handleMessage(self):
        if self.data is None:
            self.data = ''
        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print n
         
    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'
      

def serverThread(serverObject, port):
    print "EchoServer on port "+str(port)+" Online"
    serverObject.serveforever()


if __name__ == "__main__":
    server1 = SimpleWebSocketServer('', 23019, SimpleEcho)
    server2 = SimpleWebSocketServer('', 23193, SimpleEcho)
    server3 = SimpleWebSocketServer('', 47913, SimpleEcho)
    serverObject1 = Thread(target = serverThread, args = (server1,23019))
    serverObject2 = Thread(target = serverThread, args = (server2,23193))
    serverObject3 = Thread(target = serverThread, args = (server3,47913))
    serverObject1.start()
    serverObject2.start()
    serverObject3.start()


