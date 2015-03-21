import unittest
from pkgMissionControl.implementation.Launcher import Assistance
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient



class TestAssistance(unittest.TestCase):

    def testEchoVerbose(self):
        instance = Assistance()
        # request echo
        dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
        dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world!\n'+'none\n'+'none\n'+'immediate\n'+'none\n')
        print "data verboselly sent"
        ticket = dummySocket.receiveData()
        dummySocket.close()
        self.assertEqual(ticket, "0123")
        print "it worked"
        instance.shutdown()
        
    
if __name__ == '__main__':
    unittest.main()