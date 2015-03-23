import unittest, time
import pkgMissionControl.implementation.Launcher
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient



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
        pkgMissionControl.implementation.Launcher.setup()
        try:
            # request echo
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world!\n'+'none\n'+'none\n'+'immediate\n'+'none\n')
            print "data verboselly sent\n"
            ticket1 = dummySocket.receiveData()
            dummySocket.close()
            
            print ""
            time.sleep(2)
            
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world 2!\n'+'none\n'+'none\n'+'immediate\n'+'none\n')
            print "more data verboselly sent\n"
            ticket2 = dummySocket.receiveData()
            dummySocket.close()
                        
            self.assertEqual(ticket1, "testTicket1")
            self.assertEqual(ticket2, "testTicket2")
            
            print "it worked"
            pkgMissionControl.implementation.Launcher.getOfficerInstance().printTaskBuffer()
        finally:
            pkgMissionControl.implementation.Launcher.shutdown()
        
    
if __name__ == '__main__':
    unittest.main()