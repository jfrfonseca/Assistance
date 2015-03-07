import time
from WebSocketThreadObject import WebSocketThreadObject  # @UnresolvedImport

verificationInterval = 0.02

print "setting up echo server"
echoServer = WebSocketThreadObject(23019)
print "Echo server all set up!"

print "getting messages:"
message = ''
while message == '':
    time.sleep(verificationInterval)
    message = echoServer.getMessagesBuffer()[0]
print "we've got messages!"
print "message: "+message
print "sending echo back"
echoServer.sendMessage(message)
print "all done" 

echoServer.printTest()
