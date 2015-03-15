
import unittest, os, sys
from transceiver.implementation.Transceiver import Transceiver
from cpnCommonLibraries.AssistanceSockets import AssistanceSocketClient, AssistanceSocketServer

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '...'))
if not path in sys.path:
    sys.path.insert(1, path)
del path


class TestTransceiverObject(unittest.TestCase):
    transceiver = ''
    dummySocket = ''
    
    def setUp(self):
        self.transceiver = Transceiver()
        
    def tearDown(self):
        self.transceiver.shutdown()

    
    def test_programCalling(self):
        self.dummySocket = AssistanceSocketClient('', 29112, '0123456789ABCDEF')
        self.dummySocket.sendData('HS it worked')
        recovered = self.dummySocket.receiveData()
        self.dummySocket.close()
        self.assertEqual(recovered, 'HS it worked'.upper())
    
if __name__ == '__main__':
    unittest.main()