import time, os, sys
from cpnCommonLibraries.WebSocketThreadObject import WebSocketThreadObject  # @UnresolvedImport

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '...'))
if not path in sys.path:
    sys.path.insert(1, path)
del path


class Transceiver:
    global bibliothekarAntenna, torAntenna, fernTransceiverAntenna
    
    def __init__(self, bibliothekarAntennaPort, torAntennaPort, fernTransceiverAntennaPort):
        #self.bibliothekarAntenna = WebSocketThreadObject('', bibliothekarAntennaPort)
        self.torAntenna = WebSocketThreadObject('', torAntennaPort)
        #self.fernTransceiverAntenna = WebSocketThreadObject('', fernTransceiverAntennaPort)
        
        
    def getbibliothekarAntennaServer(self):
        return self.bibliothekarAntenna.getServerObject()    
    
    
    def testEchoServer(self):
        print "setting up WebSocket echo server on port "+str(self.torAntenna.getPort())     
        print "waiting for messages:"
        message = ''
        repetitions = 6
        while repetitions > 0:
            while message == '':
                time.sleep(0.02)
                message = self.torAntenna.getReceivedMessagesBuffer()[0]
            print "we've got messages!"
            print "message: "+message
            print "sending echo back"
            self.torAntenna.sendMessage(message)
            print "all done, but it can be done only "+str(repetitions)+" more times"
            self.torAntenna.clearMessagesBuffer()
            message = ''
            repetitions -= 1
        print "Done testing the Tor -||- Transceiver WebSocket"
        self.torAntenna.concludere()