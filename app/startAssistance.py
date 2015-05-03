#!/usr/bin/env python
'''
Performs series of tests to the Assistance Project
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
from optparse import OptionParser
# ASSISTANCE MODULE IMPORTS ----------
import Assistance
from pkgMissionControl.implementation import Launcher
# ASSISTANCE CONSTANTS IMPORTS ----
from IOUtils import saveAll
from UnitTests import AssistanceUnitTests
from cpnLibrary.implementation.Constants import SCHEDULE_FIFO, SCHEDULE_NONE


'''
Runs this file
'''
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--server",
                      dest="isServer", action="store_true",
                      help="Starts a Assistance Server in this machine")
    parser.add_option("-n", "--myName",
                      dest="myName", action="store", type="string",
                      help="Names the Assistance LOGs in this machine")
    parser.add_option("-f", "--client-functionality",
                      dest="isFunctionality", action="store_true",
                      help="Sets this machine as a Test Client of the functionality of Assistance in this LAN")  # @IgnorePep8
    parser.add_option("-a", "--assistanceServer",
                      dest="peerIPs", action="append", type="string",
                      help="List of the IPs of Assistance Servers in this LAN")  # @IgnorePep8
    parser.add_option("--fifo",
                      dest="isFIFO", action="store_true",
                      help="Sets this instance's scheduling scheme as FIFO")  # @IgnorePep8
    (options, args) = parser.parse_args()

    scheduling = SCHEDULE_NONE
    if options.isFIFO:
        scheduling = SCHEDULE_FIFO

    if options.myName is None:
        myname = ''
    else:
        myname = options.myName+"-"+scheduling

    if options.isServer:
        Assistance.setup(SCHEDULE_FIFO)
        stall = raw_input("\nAssistance Server '"+myname+"' Up! Press ENTER to finish")  # @UnusedVariable @IgnorePep8
        Launcher.getOfficerInstance().saveLogs()
        saveAll(myname)
        Assistance.shutdown()

    if options.peerIPs is None:
        ipList = ['']
    else:
        ipList = options.peerIPs

    if options.isFunctionality:
        localFuncTest = AssistanceUnitTests()
        localFuncTest.setUp()
        localFuncTest.testNetworkFunc(ipList)
        localFuncTest.tearDown(myname)
