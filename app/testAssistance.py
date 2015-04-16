import unittest
import Assistance
from pkgMissionControl.implementation import Launcher
from tests import SHA256Test, SHA256remoteTest, EchoTest

class TestAssistance(unittest.TestCase):
    
    # Starts the Assistance Service
    def setUp(self):        
        Assistance.setup()
        
    # Finishes the Assistance Service  
    def tearDown(self):      
        #time.sleep(10)  
        print "All tests are done. Saving  the LOGs and closing up"
        Launcher.getOfficerInstance().saveLogs() 
        Assistance.shutdown()
        
    # Test the local echo - submit and recover tickets, check the status, and synchronises each ticket.
    def test(self):        
        print "Echo Test"        
        ticket1 = EchoTest.request("Hello World")
        ticket2 = EchoTest.request("Hello, World!")
        ticket3 = EchoTest.request("HeII0, W0r1d!!!111!")
        print "Tickets: "
        print ticket1
        print ticket2
        print ticket3
        print "Status: "
        print EchoTest.checkStatus(ticket1)
        print EchoTest.checkStatus(ticket2)
        print EchoTest.checkStatus(ticket3)
        print "Synch: "
        print EchoTest.synch(ticket1)
        print EchoTest.synch(ticket2)
        print EchoTest.synch(ticket3)
        
        print "\nSHA256 test"
        ticket3 = SHA256Test.request()
        ticket4 = SHA256Test.request()
        print "Tickets: "
        print ticket3
        print ticket4
        print "Status: "
        print SHA256Test.checkStatus(ticket3)
        print SHA256Test.checkStatus(ticket4)
        print "Synch: "
        print SHA256Test.synch(ticket3)
        print SHA256Test.synch(ticket4)
        
        print "\nSHA256 by Remote File test"
        ticket5 = SHA256remoteTest.request("/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")
        ticket6 = SHA256remoteTest.request("/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")
        print "Tickets: "
        print ticket5
        print ticket6
        print "Status: "
        print SHA256remoteTest.checkStatus(ticket5)
        print SHA256remoteTest.checkStatus(ticket6)
        print "Submitting data "
        SHA256remoteTest.submit(ticket5, "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")
        SHA256remoteTest.submit(ticket6, "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")
        print "Synch: "
        print SHA256remoteTest.synch(ticket5)
        print SHA256remoteTest.synch(ticket6)
        
        #time.sleep(10)
    
        
    
if __name__ == '__main__':
    unittest.main()      