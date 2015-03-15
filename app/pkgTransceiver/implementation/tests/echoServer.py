import time
from WebSocketThreadObject import WebSocketThreadObject  # @UnresolvedImport

def testEchoServer (testPort):
    print "setting up echo server on port "+str(testPort)
    echoServer = WebSocketThreadObject('', testPort)
    print "Echo server all set up!"
    
    print "getting messages:"
    message = ''
    while 1:
        while message == '':
            time.sleep(0.02)
            message = echoServer.getMessagesBuffer()[0]
        print "we've got messages!"
        print "message: "+message
        print "sending echo back"
        echoServer.sendMessage(message)
        print "all done"
        echoServer.clearMessagesBuffer()
        message = ''

