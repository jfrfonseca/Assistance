#!/usr/bin/env python
'''
Performer.py - Class of the AssistancePerformer Package with the functions to
execute a task from the Assistance Officer
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import unittest
import zipfile
import os
# ASSISTANCE MODULE IMPORTS ----------
import Assistance
# ASSISTANCE OBJECT IMPORTS ------------
from pkgMissionControl.implementation import Launcher
from tests import SHA256Test, SHA256remoteTest, EchoTest


class TestAssistance(unittest.TestCase):  # @IgnorePep8
    '''
    A series of Unit Tests to the Functionality of the Assistance System
    '''

    def zipdir(self, path, zipf):
        '''
        Adds a directory to a zip file
        :param path: relative path to the file
        :param zipf: zipfile object to the directory to be added to
        '''
        for root, dirs, files in os.walk(path):  # @UnusedVariable
            for fileObj in files:
                zipf.write(os.path.join(root, fileObj))

    def setUp(self):
        '''
        Starts the Assistance Service
        '''
        Assistance.setup()

    def tearDown(self):
        '''
        Shuts down Assistance Service
        '''
        print "All tests are done. Saving  the LOGs"
        Launcher.getOfficerInstance().saveLogs()
        zipf = zipfile.ZipFile('LOGs.zip', 'w')
        self.zipdir('LOG/', zipf)
        self.zipdir('AssistanceApps/outputs/', zipf)
        self.zipdir('tests/', zipf)
        zipf.close()
        print "Created ZIP file"
        Assistance.shutdown()
        print "Finished everything"

    def test(self):
        '''
        Basic functionality tests:
            request a ticket (in 3 different apps, 2-3 times each)
            checks the status of the task (probably it will be "waiting")
            synchronizes the results
        The EchoTest app sends a string, and receives it back in all caps.
            All as immediates. The performer runs in python
        The SHA256test sends the path to a local file to a pre-compiled C app,
            that outputs the results in files, and returns the paths to stderr and stdout back  # @IgnorePep8
        The SHA256remoteTest does almost the same that the last test, but this time,  # @IgnorePep8
            a file is submit by a socket and the results are returned by another  # @IgnorePep8
        '''
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
        ticket5 = SHA256remoteTest.request(
            "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")  # @IgnorePep8
        ticket6 = SHA256remoteTest.request(
            "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")  # @IgnorePep8
        print "Tickets: "
        print ticket5
        print ticket6
        print "Status: "
        print SHA256remoteTest.checkStatus(ticket5)
        print SHA256remoteTest.checkStatus(ticket6)
        print "Submitting data "
        SHA256remoteTest.submit(
            ticket5,
            "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")  # @IgnorePep8
        SHA256remoteTest.submit(
            ticket6,
            "/home/zeff/Dropbox/ActiveWorkspace/Assistance/app/AssistanceApps/sha256/V0.5/tests/experimentData.dat")  # @IgnorePep8
        print "Synch: "
        print SHA256remoteTest.synch(ticket5)
        print SHA256remoteTest.synch(ticket6)


'''
Runs this file
'''
if __name__ == '__main__':
    unittest.main()
