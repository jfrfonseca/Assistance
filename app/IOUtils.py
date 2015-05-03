#!/usr/bin/env python
'''
Permits better IO with the Assistance instance in the local machine
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import zipfile
import os
import threading
# ASSISTANCE CONSTANTS IMPORTS ----
from cpnLibrary.implementation.Constants import DIR_APPS_CWD


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


def saveAll(myname=''):
    '''
    Shuts down Assistance Service
    '''
    print("All tests are done. Saving LOGs"+myname+".zip")
    zipf = zipfile.ZipFile('LOGs'+myname+'.zip', 'a')
    zipdir('LOG/', zipf)
    zipdir(DIR_APPS_CWD, zipf)
    zipdir('testsResults/', zipf)
    zipdir('testsData/', zipf)
    zipf.close()