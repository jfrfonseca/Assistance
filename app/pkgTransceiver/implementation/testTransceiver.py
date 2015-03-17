
import unittest, os, sys
from pkgTransceiver.implementation.Transceiver import Transceiver
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '...'))
if not path in sys.path:
    sys.path.insert(1, path)
del path


class TestTransceiverObject(unittest.TestCase):
    
#    def test_programCalling(self):
#        self.dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
#        self.dummySocket.sendData('HS it worked')
#        print "data sent"
#        recovered = self.dummySocket.receiveData()
#        self.dummySocket.close()
#        self.assertEqual(recovered, 'HS it worked'.upper())

    def testTicket(self):
        transceiver = Transceiver()
        dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
        dummySocket.sendData('echo\n'+'immediate\n'+'hello world!\n'+'none\n'+'none\n')
        print "data sent"
        recovered = dummySocket.receiveData()
        dummySocket.close()
        self.assertEqual(recovered, "0123")
        print "it worked"
        transceiver.shutdown()
         
    
if __name__ == '__main__':
    unittest.main()