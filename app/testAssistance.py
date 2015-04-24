#!/usr/bin/env python
'''
Performer.py - Class of the AssistancePerformer Package with the functions to
execute a task from the Assistance Officer
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import zipfile
import os
import time
import threading
import multiprocessing
from optparse import OptionParser
# ASSISTANCE MODULE IMPORTS ----------
import Assistance
# ASSISTANCE OBJECT IMPORTS ------------
from pkgMissionControl.implementation import Launcher
import SHA256Test
import SHA256remoteTest
import EchoTest
import WEKA
# ASSISTANCE CONSTANTS IMPORTS ----
from cpnLibrary.implementation.Constants import DIR_APPS_CWD
# LOCAL CONSTANTS ---------------------------
TIME_WATCHDOG = 5
MANUAL = "\nUsage:"\
    + "\n\t ./testAssistance -server"\
    + "\n\t ./testAssistance -client (-functionality | -fullExperiment)"\
    + " (-local | ['one or more servers IPs in the local LAN'])"

'''
A series tests to the Assistance System
'''


class ResultsPrinter():
    def __init__(self, logFileName, mode='a'):
        self.ioFile = open(logFileName, mode)
        self.active = True
        self.printBuffer = []
        self.lock = threading.Event()
        self.printerThread = threading.Thread(target=self.printerServer)

    def printerServer(self):
        while(self.active):
            if len(self.printBuffer) > 0:
                toPrint = self.printBuffer.pop(0)
                self.ioFile.write(toPrint+'\n')
            else:
                self.lock.wait()
                self.lock.clear()

    def shutdown(self):
        self.active = False
        while len(self.printBuffer) > 0:
            toPrint = self.printBuffer.pop(0)
            print toPrint
            self.ioFile.write(toPrint+'\n')
        self.ioFile.close()

    def dual_print(self, string2Print):
        print string2Print
        self.printBuffer.append(string2Print)
        self.lock.set()


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

    def tearDown(self):
        '''
        Shuts down Assistance Service
        '''
        self.printer.shutdown()
        Launcher.getOfficerInstance().saveLogs()
        saveAll()
        Assistance.shutdown()
        print("Finished everything")

    def testFuncionality(self, peerIP='127.0.0.1'):
        testSuite = ['Echo', 'SHA256LocalFile', 'SHA256FTP', 'WEKAfunctionality']  # @IgnorePep8
        testsArray = []
        testsResults = multiprocessing.Queue()
        for testName in testSuite:
            singleTest = getattr(self, testName)
            process = multiprocessing.Process(target=singleTest, args=(testsResults, peerIP,))  # @IgnorePep8
            testsArray.append(process)
            process.start()
        time.sleep(TIME_WATCHDOG)
        for testNum in range(len(testSuite)):
            if testsArray[testNum].is_alive():
                testsArray[testNum].terminate()
                self.printer.dual_print("WatchdogThread<TestFunctionality>::: ######## ERROR! ######## Test "  # @IgnorePep8
                                        + testSuite[testNum] + " to "+peerIP+" has timed-out, (not ended in "+TIME_WATCHDOG+" seconds) and was terminated.")  # @IgnorePep8
            else:
                self.printer.dual_print("WatchdogThread<TestFunctionality>:::Test "  # @IgnorePep8
                                        + testSuite[testNum] + " to "+peerIP+" has ended successfully.")  # @IgnorePep8
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
        results += '\n' + (WEKA.synch(ticket7, peerIP))
        results += '\n' + (WEKA.synch(ticket8, peerIP))
        results += "\n<END>"
        resultsBuffer.put(results)


def zipdir(path, zipf):
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


def saveAll():
    '''
    Shuts down Assistance Service
    '''
    print("All tests are done. Saving  the LOGs")
    zipf = zipfile.ZipFile('LOGs.zip', 'a')
    zipdir('LOG/', zipf)
    zipdir(DIR_APPS_CWD, zipf)
    zipdir('testsResults/', zipf)
    zipdir('testsData/', zipf)
    zipf.close()


'''
Runs this file
'''
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--server",
                      dest="isServer", action="store_true",
                      help="Starts a Assistance Server in this machine")
    parser.add_option("-e", "--client-experiment",
                      dest="isExperiment", action="store_true",
                      help="Sets this machine as a Test Client of the Assistance Experiment in this LAN for each of the IPs provided in this option.")  # @IgnorePep8
    parser.add_option("-f", "--client-functionality",
                      dest="isFunctionality", action="store_true",
                      help="Sets this machine as a Test Client of the functionality of Assistance in this LAN")  # @IgnorePep8
    parser.add_option("-a", "--assistanceServer",
                      dest="peerIPs", action="append", type="string",
                      help="List of the IPs of Assistance Servers in this LAN")  # @IgnorePep8
    (options, args) = parser.parse_args()

    if options.isServer:
        Assistance.setup()
        stall = raw_input("\nAssistance Server Up! Press ENTER to finish")  # @UnusedVariable @IgnorePep8
        Launcher.getOfficerInstance().saveLogs()
        saveAll()
        Assistance.shutdown()
    if options.peerIPs is None:
        ipList = ['']
    else:
        ipList = options.peerIPs
    if options.isFunctionality:
        localFuncTest = AssistanceUnitTests()
        localFuncTest.setUp()
        for peerIP in ipList:
            localFuncTest.testFuncionality(peerIP)
        localFuncTest.tearDown()
    #elif options.isExperiment:
    #    stall=1
