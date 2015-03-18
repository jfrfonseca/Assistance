import unittest
import launch
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient



class TestAssistance(unittest.TestCase):

    def testEcho(self):
        instance = launch.Assistance()
        # request echo
        dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
        dummySocket.sendData('ASSISTANCE_ECHO_TEST\n'+'immediate\n'+'hello world!\n'+'none\n'+'none\n')
        print "data sent"
        ticket = dummySocket.receiveData()
        dummySocket.close()
        self.assertEqual(ticket, "0123")
        print "it worked"
    
if __name__ == '__main__':
    unittest.main()