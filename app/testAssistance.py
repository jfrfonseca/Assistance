import unittest, time
import Assistance
from pkgMissionControl.implementation import Launcher
from tests import LocalEchoTest, SHA256Test

class TestAssistance(unittest.TestCase):

    """def testTwoEchoesVerbose(self):
        Assistance.setup()
        try:
            # request echo
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            print "socket Created"
            dummySocket.sendData(()
            print "data sent\n"
            ticket1 = dummySocket.receiveData()
            dummySocket.close()
            
            print ""
            #time.sleep(2)
            
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            dummySocket.sendMessage(AssistanceDBMS.getSymbol("API_REQUEST_MSG", "MESSAGE_KIND"), 'ASSISTANCE_ECHO_TEST\n'+'hello world again!\n'+AssistanceDBMS.getSymbol('NONE')+'\n'+AssistanceDBMS.getSymbol('NONE')+'\n')
            print "more data sent\n"
            ticket2 = dummySocket.receiveData()[2]
            # the test below will not work, since the handler class only finishes dealing with a connection once it is closed
            #dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world and all who live upon it!\n'+'none\n'+'none\n')
            #print "more data sent, but without closing the socket first! \n"
            #ticket3 = dummySocket.receiveData()
            dummySocket.close()
                        
            dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
            dummySocket.sendMessage(AssistanceDBMS.getSymbol("API_REQUEST_MSG", "MESSAGE_KIND"), 'ASSISTANCE_SHA256_TEST\n'+AssistanceDBMS.getSymbol('NONE')+'\n'+AssistanceDBMS.getSymbol('LOCAL_FILE', 'CHANNEL')+'\n'+'/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat'+'\n')
            print "requesting a SHA256 that SHOUD take a second to run!\n"
            ticket4 = dummySocket.receiveData()
            dummySocket.close()
                        
            self.assertEqual(ticket1, "testTicket1")
            self.assertEqual(ticket2, "testTicket2")
            #self.assertEqual(ticket3, "testTicket3")
            self.assertEqual(ticket4, "testTicket3")
            
            time.sleep(2)
            
            # check echo 
            dummySocket = AssistanceSocketClient('', 21902, '0123456789ABCDEF')
            dummySocket.sendData('STATUS_CHECK\n'+'testTicket1\n')
            print "status check for ticket 1 sent!\n"
            status1 = dummySocket.receiveData()
            dummySocket.close()
            
            dummySocket = AssistanceSocketClient('', 21902, '0123456789ABCDEF')
            dummySocket.sendData('STATUS_CHECK\n'+'testTicket3\n')
            print "status check for ticket 3 sent!\n"
            status3 = dummySocket.receiveData()
            dummySocket.close()
            
            print "The status for the first call to Assistance Echo Test, service ticket "+ticket1+" is: "+status1
            print "The status for the first call to Assistance SHA256 Test, service ticket "+ticket4+" is: "+status3
            
            print "If we got here, it means that all the inner Assistance Echo Caps tests AND the SHA256 test were completed successfully. Now, you can run the external test, and check the logs"
            
            #timeToFinish = raw_input("When you are done testing, type 'finish' and 'enter' in this window - ")
            #while timeToFinish != 'finish':
            #    print "you entered: "+timeToFinish
            #    timeToFinish = raw_input("When you are done testing, type 'finish' and 'enter' in this window - ")

            
            Launcher.getOfficerInstance().printLogs()
        finally:
            Assistance.shutdown()            
            print "it worked"
        """
        
    def test_DoAllTests(self):        
        Assistance.setup()
        #Two Echoes test
        ticket1 = LocalEchoTest.request("Hello World")
        ticket2 = LocalEchoTest.request("Hello, World!")
        self.assertEqual(ticket1, "testTicket1")
        self.assertEqual(ticket2, "testTicket2")
        #Two SHA256 tests
        ticket3 = SHA256Test.request()
        ticket4 = SHA256Test.request()
        self.assertEqual(ticket3, "testTicket3")
        self.assertEqual(ticket4, "testTicket4")
        
        time.sleep(3)
        Launcher.getOfficerInstance().printLogs()        
        print "it worked"
        Assistance.shutdown()
        
    
if __name__ == '__main__':
    unittest.main()
    Assistance.shutdown()