import unittest, time
import Assistance
from pkgMissionControl.implementation import Launcher
from tests import LocalEchoTest, SHA256Test, SHA256remoteTest
import os

class TestAssistance(unittest.TestCase):
    
    # Starts the Assistance Service
    def setUp(self):        
        Assistance.setup()
        
    # Finishes the Assistance Service  
    def tearDown(self):        
        print "All tests are done. Saving  the LOGs and closing up"
        Launcher.getOfficerInstance().saveLogs() 
        Assistance.shutdown()
        
    # Test the local echo - submit and recover tickets, check the status, and synchronises each ticket.
    def test_Echo(self):        
        print "Echo Test"        
        ticket1 = LocalEchoTest.request("Hello World")
        ticket2 = LocalEchoTest.request("Hello, World!")
        print "Tickets: "
        print ticket1
        print ticket2
        print "Status: "
        print LocalEchoTest.checkStatus(ticket1)
        print LocalEchoTest.checkStatus(ticket2)
        print "Synch: "
        print LocalEchoTest.synchronise(ticket1)
        print LocalEchoTest.synchronise(ticket2)
        
    # Tests
    #def test_SHA256(self):
        print "SHA256 test"
        ticket3 = SHA256Test.request()
        ticket4 = SHA256Test.request()
        print "Tickets: "
        print ticket3
        print ticket4
        print "Status: "
        print SHA256Test.checkStatus(ticket3)
        print SHA256Test.checkStatus(ticket4)
        print "Synch: "
        print SHA256Test.synchronise(ticket3)
        print SHA256Test.synchronise(ticket4)
        
    
if __name__ == '__main__':
    unittest.main()      