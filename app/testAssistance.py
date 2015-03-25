import unittest, time
import Assistance
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient
from pkgMissionControl.implementation import Launcher



class TestAssistance(unittest.TestCase):

#    def testEchoVerbose(self):
#        pkgMissionControl.implementation.Launcher.setup()
#        # request echo
#        dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
#        dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world!\n'+'none\n'+'none\n'+'immediate\n'+'none\n')
#        print "data verboselly sent"
#        ticket = dummySocket.receiveData()
#        dummySocket.close()
#        self.assertEqual(ticket, "0123")
#        print "it worked"
#        pkgMissionControl.implementation.Launcher.shutdown()
        
    def testTwoEchoesVerbose(self):
        Assistance.setup()
        try:
            # request echo
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world!\n'+'none\n'+'none\n')
            print "data sent\n"
            ticket1 = dummySocket.receiveData()
            dummySocket.close()
            
            print ""
            #time.sleep(2)
            
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world again!\n'+'none\n'+'none\n')
            print "more data sent\n"
            ticket2 = dummySocket.receiveData()
            # the test below will not work, since the handler class only finishes dealing with a connection once it is closed
            #dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world and all who live upon it!\n'+'none\n'+'none\n')
            #print "more data sent, but without closing the socket first! \n"
            #ticket3 = dummySocket.receiveData()
            dummySocket.close()
                        
            self.assertEqual(ticket1, "testTicket1")
            self.assertEqual(ticket2, "testTicket2")
            #self.assertEqual(ticket3, "testTicket3")
            
            print "it worked"
            
            time.sleep(2)
            
            Launcher.getOfficerInstance().printLogs()
        finally:
            Assistance.shutdown()
        
    
if __name__ == '__main__':
    unittest.main()
    Assistance.shutdown()