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
import SHA256Test
import SHA256remoteTest
import EchoTest
import WEKA


class TestDiagnose(unittest.TestCase):  # @IgnorePep8
    '''
    A series of Unit Tests to the Functionality of the Assistance System
    '''

    def dual_print(self, string2Print):
        '''
        Print a string both to a file and to the screen
        :param string2Print: string to print
        '''
        self.ioFile.write(string2Print+'\n')
        print string2Print

    def zipdir(self, path, zipf):
        '''
        Adds a directory to a zip file
        :param path: relative path to the file
        :param zipf: zipfile object to the directory to be added to
        '''
        filesIn = zipf.namelist()
        for fileNum in range(len(filesIn)):
            filesIn[fileNum] = filesIn[fileNum].split('/')[-1]
        for root, dirs, files in os.walk(path):  # @UnusedVariable
            for fileObj in files:
                if fileObj not in filesIn:
                    if not fileObj.endswith('~'):
                        zipf.write(os.path.join(root, fileObj))

    def setUp(self):
        '''
        Starts the Assistance Service
        '''
        self.ioFile = open("LOG/ioFile.txt", 'w')
        self.AssistanceInstance = Assistance()

    def tearDown(self):
        '''
        Shuts down Assistance Service
        '''
        self.dual_print("All tests are done. Saving  the LOGs")
        self.ioFile.close()
        self.AssistanceInstance.getOfficerInstance().saveLogs()
        zipf = zipfile.ZipFile('LOGs.zip', 'a')
        self.zipdir('LOG/', zipf)
        self.zipdir('AssistanceApps/data/', zipf)
        self.zipdir('AssistanceApps/outputs/', zipf)
        self.zipdir('testsResults/', zipf)
        self.zipdir('testsData/', zipf)
        zipf.close()
        print("Created ZIP file")
        self.AssistanceInstance.shutdown()
        print("Finished everything")

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
        self.dual_print("Echo Test")
        ticket1 = EchoTest.request("Hello World")
        ticket2 = EchoTest.request("Hello, World!")
        ticket3 = EchoTest.request("HeII0, W0r1d!!!111!")
        self.dual_print("Tickets: ")
        self.dual_print(ticket1)
        self.dual_print(ticket2)
        self.dual_print(ticket3)
        self.dual_print("Status: ")
        self.dual_print(EchoTest.checkStatus(ticket1))
        self.dual_print(EchoTest.checkStatus(ticket2))
        self.dual_print(EchoTest.checkStatus(ticket3))
        self.dual_print("Synch: ")
        self.dual_print(EchoTest.synch(ticket1))
        self.dual_print(EchoTest.synch(ticket2))
        self.dual_print(EchoTest.synch(ticket3))

        self.dual_print("\nSHA256 test")
        ticket3 = SHA256Test.request()
        ticket4 = SHA256Test.request()
        self.dual_print("Tickets: ")
        self.dual_print(ticket3)
        self.dual_print(ticket4)
        self.dual_print("Status: ")
        self.dual_print(SHA256Test.checkStatus(ticket3))
        self.dual_print(SHA256Test.checkStatus(ticket4))
        self.dual_print("Synch: ")
        self.dual_print(SHA256Test.synch(ticket3))
        self.dual_print(SHA256Test.synch(ticket4))

        self.dual_print("\nSHA256 by Remote File test")
        ticket5 = SHA256remoteTest.request(
            "testsData/experimentData.dat")  # @IgnorePep8
        ticket6 = SHA256remoteTest.request(
            "testsData/experimentData.dat")  # @IgnorePep8
        self.dual_print("Tickets: ")
        self.dual_print(ticket5)
        self.dual_print(ticket6)
        self.dual_print("Status: ")
        self.dual_print(SHA256remoteTest.checkStatus(ticket5))
        self.dual_print(SHA256remoteTest.checkStatus(ticket6))
        self.dual_print("Submitting data ")
        SHA256remoteTest.submit(
            ticket5,
            "testsData/experimentData.dat")  # @IgnorePep8
        SHA256remoteTest.submit(
            ticket6,
            "testsData/experimentData.dat")  # @IgnorePep8
        self.dual_print("Synch: ")
        self.dual_print(SHA256remoteTest.synch(ticket5))
        self.dual_print(SHA256remoteTest.synch(ticket6))

        self.dual_print("\nWEKA J48 tree classifier by Remote File test")
        ticket7 = WEKA.request("weka.classifiers.trees.J48",
                               "-t",
                               "testsData/weather.nominal.arff")
        ticket8 = WEKA.request("weka.classifiers.trees.J48",
                               "-t",
                               "testsData/weather.numeric.arff")
        self.dual_print("Tickets: ")
        self.dual_print(ticket7)
        self.dual_print(ticket8)
        self.dual_print("Status: ")
        self.dual_print(WEKA.checkStatus(ticket7))
        self.dual_print(WEKA.checkStatus(ticket8))
        self.dual_print("Submitting data ")
        WEKA.submit(
            ticket7,
            "testsData/weather.nominal.arff")
        WEKA.submit(
            ticket8,
            "testsData/weather.numeric.arff")
        self.dual_print("Synch: ")
        self.dual_print(WEKA.synch(ticket7))
        self.dual_print(WEKA.synch(ticket8))


'''
Runs this file
'''
if __name__ == '__main__':
    unittest.main()
