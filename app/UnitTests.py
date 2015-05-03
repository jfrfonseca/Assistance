#!/usr/bin/env python
'''
Performs series of tests to the Assistance Project
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import multiprocessing
# ASSISTANCE MODULE IMPORTS ----------
import Assistance
from pkgMissionControl.implementation import Launcher
import SHA256Test
import SHA256remoteTest
import EchoTest
import WEKA
from IOUtils import ResultsPrinter, saveAll
# LOCAL CONSTANTS ---------------------------
TIME_WATCHDOG = 30


class AssistanceUnitTests():
    '''
    A series of Unit Tests to the Assistance System
    '''

    def setUp(self):
        '''
        Starts the Assistance Service
        '''
        self.printer = ResultsPrinter("LOG/terminalIO.log")
        Assistance.setup()

    def tearDown(self, myname=''):
        '''
        Shuts down Assistance Service
        '''
        self.printer.shutdown()
        Launcher.getOfficerInstance().saveLogs()
        saveAll(myname)
        Assistance.shutdown()
        print("Finished everything")

    def testFuncionality(self, bigResults, peerIP):
        testSuite = ['Echo', 'SHA256LocalFile', 'SHA256FTP', 'WEKAfunctionality']  # @IgnorePep8
        testsArray = []
        testsResults = multiprocessing.Queue()
        for testName in testSuite:
            singleTest = getattr(self, testName)
            process = multiprocessing.Process(target=singleTest, args=(testsResults, peerIP,))  # @IgnorePep8
            testsArray.append(process)
            process.start()
        time.sleep(TIME_WATCHDOG)
        myresults = '\n'
        for testNum in range(len(testSuite)):
            if testsArray[testNum].is_alive():
                testsArray[testNum].terminate()
                myresults += ("\nWatchdogThread<TestFunctionality><"+str(peerIP)+">::: ######## ERROR! ######## Test "  # @IgnorePep8
                                        + testSuite[testNum] + " has timed-out, (not ended in "+str(TIME_WATCHDOG)+" seconds) and was terminated.")  # @IgnorePep8
            else:
                myresults += ("\nWatchdogThread<TestFunctionality><"+str(peerIP)+">:::Test "  # @IgnorePep8
                                        + testSuite[testNum] + " has ended successfully.")  # @IgnorePep8
        results = [testsResults.get() for process in testsArray]
        for line in results:
            myresults += '\n' + line
        bigResults.put(myresults)

    def testNetworkFunc(self, peerList=['127.0.0.1']):
        testsArray = []
        testsResults = multiprocessing.Queue()
        for peerIP in peerList:
            process = multiprocessing.Process(target=self.testFuncionality, args=(testsResults, peerIP,))  # @IgnorePep8
            testsArray.append(process)
            process.start()
        print "\n\nJust sent the tests. Waiting.\n"
        time.sleep(TIME_WATCHDOG)
        time.sleep(TIME_WATCHDOG)
        results = [testsResults.get() for process in testsArray]
        for line in results:
            self.printer.dual_print(line)

    def Echo(self, resultsBuffer, peerIP='127.0.0.1'):
        results = "\n<BEGIN><Echo><"+peerIP+">"
        ticket1 = EchoTest.request("Hello World", peerIP)
        ticket2 = EchoTest.request("Hello, World!", peerIP)
        ticket3 = EchoTest.request("HeII0, W0r1d!!!111!", peerIP)
        results += '\n' + ("Tickets: ")
        results += '\n' + (ticket1)
        results += '\n' + (ticket2)
        results += '\n' + (ticket3)
        results += '\n' + ("Status: ")
        results += '\n' + (EchoTest.checkStatus(ticket1, peerIP))
        results += '\n' + (EchoTest.checkStatus(ticket2, peerIP))
        results += '\n' + (EchoTest.checkStatus(ticket3, peerIP))
        results += '\n' + ("Synch: ")
        results += '\n' + (EchoTest.synch(ticket1, peerIP))
        results += '\n' + (EchoTest.synch(ticket2, peerIP))
        results += '\n' + (EchoTest.synch(ticket3, peerIP))
        results += "\n<END>"
        resultsBuffer.put(results)

    def SHA256LocalFile(self, resultsBuffer, peerIP='127.0.0.1'):  # @UnusedVariable , DAAAH! @IgnorePep8
        results = "\n<BEGIN><SHA256LocalFile><127.0.0.1>"
        ticket3 = SHA256Test.request()
        ticket4 = SHA256Test.request()
        results += '\n' + ("Tickets: ")
        results += '\n' + (ticket3)
        results += '\n' + (ticket4)
        results += '\n' + ("Status: ")
        results += '\n' + (SHA256Test.checkStatus(ticket3))
        results += '\n' + (SHA256Test.checkStatus(ticket4))
        results += '\n' + ("Synch: ")
        results += '\n' + (SHA256Test.synch(ticket3))
        results += '\n' + (SHA256Test.synch(ticket4))
        results += "\n<END>"
        resultsBuffer.put(results)

    def SHA256FTP(self, resultsBuffer, peerIP='127.0.0.1'):
        results = "\n<BEGIN><SHA256FTP><"+peerIP+">"
        ticket5 = SHA256remoteTest.request(
            "testsData/experimentData.dat", peerIP)  # @IgnorePep8
        ticket6 = SHA256remoteTest.request(
            "testsData/experimentData.dat", peerIP)  # @IgnorePep8
        results += '\n' + ("Tickets: ")
        results += '\n' + (ticket5)
        results += '\n' + (ticket6)
        results += '\n' + ("Status: ")
        results += '\n' + (SHA256remoteTest.checkStatus(ticket5, peerIP))  # @IgnorePep8
        results += '\n' + (SHA256remoteTest.checkStatus(ticket6, peerIP))  # @IgnorePep8
        results += '\n' + ("Submitting data ")
        SHA256remoteTest.submit(
            ticket5,
            "testsData/experimentData.dat", peerIP)  # @IgnorePep8
        SHA256remoteTest.submit(
            ticket6,
            "testsData/experimentData.dat", peerIP)  # @IgnorePep8
        results += '\n' + ("Synch: ")
        results += '\n' + (SHA256remoteTest.synch(ticket5, peerIP))
        results += '\n' + (SHA256remoteTest.synch(ticket6, peerIP))
        results += "\n<END>"
        resultsBuffer.put(results)

    def WEKAfunctionality(self, resultsBuffer, peerIP='127.0.0.1'):
        results = "\n<BEGIN><WEKA><"+peerIP+">"
        ticket7 = WEKA.request("weka.classifiers.trees.J48",
                               "-t",
                               "testsData/weather.nominal.arff", peerIP)
        ticket8 = WEKA.request("weka.classifiers.trees.J48",
                               "-t",
                               "testsData/weather.numeric.arff", peerIP)
        results += '\n' + ("Tickets: ")
        results += '\n' + (ticket7)
        results += '\n' + (ticket8)
        results += '\n' + ("Status: ")
        results += '\n' + (WEKA.checkStatus(ticket7, peerIP))
        results += '\n' + (WEKA.checkStatus(ticket8, peerIP))
        results += '\n' + ("Submitting data ")
        WEKA.submit(
            ticket7,
            "testsData/weather.nominal.arff", peerIP)
        WEKA.submit(
            ticket8,
            "testsData/weather.numeric.arff", peerIP)
        results += '\n' + ("Synch: ")
        results7 = (WEKA.synch(ticket7, peerIP))
        results8 = (WEKA.synch(ticket8, peerIP))
        results += '\n' + results7[0] + '\n' + results7[1]
        results += '\n' + results8[0] + '\n' + results8[1]
        results += "\n<END>"
        resultsBuffer.put(results)
