#!/usr/bin/env python
'''
Performs the experiment of the Graduation of
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import multiprocessing
from optparse import OptionParser
from random import shuffle
# Assistance IMPORTS --------------------------
import GPP
import SHA256


def handleQuestGPP(resultsBuffer, quest, myname):
    results = "\n<BEGIN>\n"
    results += "<"+str(time.time())+">\n"
    results += "<GCC/GPP QUEST= "+str(quest)+">\n"
    ticket = GPP.request(quest["ARGS"], quest["DATA"],
                         quest["PEER"], myname,
                         gcc=quest["COMPILER"], zipf=quest["ZIP_CHANNEL"])
    results += str(time.time())+":::"+ticket+"\n"
    results += str(time.time())+":::BEGIN Submitting data\n"
    GPP.submit(ticket, quest["DATA"], quest["PEER"], myname)
    results += str(time.time())+":::FINISHED Submitting data\n"
    answer = GPP.synch(ticket, quest["PEER"], myname)
    results += str(time.time())+":::"+answer[0] + '\n'
    results += str(time.time())+":::"+answer[1] + '\n'
    results += "<END>"
    resultsBuffer.put(results)


def handleQuestSHA256(resultsBuffer, quest, myname):
    results = "\n<BEGIN>\n"
    results += "<"+str(time.time())+">\n"
    results += "<SHA256 QUEST= "+str(quest)+">\n"
    ticket = SHA256.request(quest["DATA"],
                            quest["ARGS"],
                            quest["PEER"])
    results += str(time.time())+":::"+ticket+"\n"
    results += str(time.time())+":::BEGIN Submitting data\n"
    SHA256.submit(ticket, quest["DATA"], quest["PEER"], myname)
    results += str(time.time())+":::FINISHED Submitting data\n"
    answer = SHA256.synch(ticket, quest["PEER"], myname)
    results += str(time.time())+":::"+answer[0] + '\n'
    results += str(time.time())+":::"+answer[1] + '\n'
    results += "<END>"
    resultsBuffer.put(results)


if __name__ == '__main__':
    # Sets up the Objects needed

    # Parses the Command-Line options
    parser = OptionParser()
    parser.add_option("-n", "--myName",
                      dest="myName", action="store", type="string",
                      help="Names the Assistance LOGs in this machine")
    parser.add_option("-t", "--timeToRun",
                      dest="timeToRun", action="store", type="string",
                      help="Sets the time to run the test")
    parser.add_option("-a", "--assistanceServer",
                      dest="peerIPs", action="append", type="string",
                      help="List of the IPs of Assistance Servers in this LAN")  # @IgnorePep8
    (options, args) = parser.parse_args()

    if options.myName is None:
        myname = ''
    else:
        myname = options.myName
    if options.peerIPs is None:
        ipList = ['']
    else:
        ipList = options.peerIPs

    TIME_WATCHDOG = 50
    if options.timeToRun is not None:
        TIME_WATCHDOG = int(options.timeToRun)

    # Forms the list of quests
    # Lists of quests parameters: APPID, ARGS, DATA files, and PEER IP
        appTouplesGPP = []
        '''
        ("", "testsData/sha256source.zip", False, True),  # @IgnorePep8
        ("-lcrypto", "testsData/hashblock.c", True, False),
        ("", "testsData/batalhanaval.c", True, False),
        ("", "testsData/blackJack.c", True, False)
        ]
    '''
    appTouplesSHA256 = [
        ("6000", "testsData/randomFile1kb"),
        ("6001", "testsData/randomFile8kb"),
        ("6002", "testsData/randomFile16kb"),
        ("2003", "testsData/randomFile128kb")
        ]

    questsListGPP = []
    questsListSHA256 = []
    for ipNum in ipList:
        for touple in appTouplesGPP:
            questsListGPP.append({
                "ARGS": touple[0],
                "DATA": touple[1],
                "PEER": ipNum,
                "COMPILER": touple[2],
                "ZIP_CHANNEL": touple[3]
                })
        for touple in appTouplesSHA256:
            questsListSHA256.append({
                "ARGS": touple[0],
                "DATA": touple[1],
                "PEER": ipNum
                })

    # Creates a new thread for each quest,
    # and commissions it by the quest handling function
    threadsArray = []
    resultsQueue = multiprocessing.Queue()
    #shuffle(questsListGPP)
    #shuffle(questsListSHA256)
    for quest in questsListGPP:
        process = multiprocessing.Process(target=handleQuestGPP, args=(resultsQueue, quest, myname,))  # @IgnorePep8
        threadsArray.append(process)
        process.start()
    for quest in questsListSHA256:
        process = multiprocessing.Process(target=handleQuestSHA256, args=(resultsQueue, quest, myname,))  # @IgnorePep8
        threadsArray.append(process)
        process.start()

    print "\n\nJust sent the tests. Waiting.\n"

    # Waits for the answers, and prints them after time out
    time.sleep(TIME_WATCHDOG)
    results = [resultsQueue.get() for process in threadsArray]
    with open(myname+".results.dat", "w") as resultsFile:
        for resultsLine in results:
            resultsFile.write(resultsLine+"\n")
            print resultsLine
