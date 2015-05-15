#!/usr/bin/env python
'''
Performs series of tests to the Assistance Project
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
from optparse import OptionParser
import socket
# ASSISTANCE MODULE IMPORTS ----------
from Assistance import Assistance
# ASSISTANCE CONSTANTS IMPORTS ----
from UnitTests import AssistanceUnitTests
from cpnLibrary.Constants import SCHEDULE_FIFO, SCHEDULE_SJF, SCHEDULE_ROUNDROBIN  # @IgnorePep8

PORT_HOTSERVER = 21982

CONFIG_HEADER = 'CONFIG'
RESET_HEADER = 'RESET'
SERVER_REST_HEADER = 'SERVER_REST'
'''
SCHEDULE_FIFO = "SCH_FIFO"
SCHEDULE_ROUNDROBIN = "SCH_RNRO"
SCHEDULE_SJF = "SCH_SJF"
'''

'''
Runs this file
'''
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--server",
                      dest="isServer", action="store_true",
                      help="Starts a Assistance Server in this machine")
    parser.add_option("--hotServer",
                      dest="isHotServer", action="store_true",
                      help="Starts a Assistance 'Hot-Swap'-able Server in this machine")  # @IgnorePep8
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
    parser.add_option("--sjf",
                      dest="isSJF", action="store_true",
                      help="Sets this instance's scheduling scheme as SJF")  # @IgnorePep8
    (options, args) = parser.parse_args()

    scheduling = SCHEDULE_ROUNDROBIN
    if options.isFIFO:
        scheduling = SCHEDULE_FIFO
    elif options.isSJF:
        scheduling = SCHEDULE_SJF

    if options.myName is None:
        myname = ''
    else:
        myname = "-"+options.myName+"-"+scheduling

    if options.isServer:
        AssistanceInstance = Assistance(scheduling)
        stall = raw_input("\nAssistance Server '"+myname+"' Up! Press ENTER to finish")  # @UnusedVariable @IgnorePep8
        AssistanceInstance.shutdown(myname)
    # <BEGIN ExperimentServer>
    elif options.isHotServer:
        logName = ''
        hotServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hotServerSocket.bind(('', PORT_HOTSERVER))
        hotServerSocket.listen(5)
        HOTSERVER_ACTIVE = True
        print "ASSISTANCE HOTSERVER ACTIVE ON PORT "+str(PORT_HOTSERVER)
        while HOTSERVER_ACTIVE:
            (clientSocket, address) = hotServerSocket.accept()
            msg = str(clientSocket.recv(1024))
            clientSocket.close()
            if msg.split(" ")[0] == CONFIG_HEADER:
                print "NEW ASSISTANCE INSTANCE '"+msg.split(" ")[1]+"' AS "+msg.split(" ")[2]  # @IgnorePep8
                logName = msg.split(" ")[1]
                AssistanceInstance = Assistance(msg.split(" ")[2], msg.split(" ")[2])
            elif msg.split(" ")[0] == RESET_HEADER:
                AssistanceInstance.shutdown(logName)
            elif msg.split(" ")[0] == SERVER_REST_HEADER:
                AssistanceInstance.shutdown(logName)
                HOTSERVER_ACTIVE = False
                print "ASSISTANCE HOTSERVER DOWN"
    # <END ExperimentServer>
    if options.peerIPs is None:
        ipList = ['']
    else:
        ipList = options.peerIPs

    if options.isFunctionality:
        localFuncTest = AssistanceUnitTests()
        localFuncTest.setUp()
        localFuncTest.testNetworkFunc(ipList)
        localFuncTest.tearDown(myname)
