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
# Assistance IMPORTS --------------------------
import WEKA
# LOCAL CONSTANTS ---------------------------
TIME_WATCHDOG = 360


def handleQuest(resultsBuffer, quest):
    results = "\n<BEGIN>\n"
    results += "<"+str(time.time())+">\n"
    ticket = WEKA.request(quest["APPID"],
                          quest["ARGS"],
                          quest["DATA"],
                          quest["PEER"])
    results += str(time.time())+":::"+ticket+"\n"
    results += str(time.time())+":::BEGIN Submitting data\n"
    WEKA.submit(ticket, quest["DATA"], quest["PEER"])
    results += str(time.time())+":::FINISHED Submitting data\n"
    answer = WEKA.synch(ticket, quest["PEER"])
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

    # Forms the list of quests
    # Lists of quests parameters: APPID, ARGS, DATA files, and PEER IP
    appTouples = [
        ("weka.classifiers.functions.SMO", "-t", "testsData/breast-cancer.arff"),  # @IgnorePep8
        ("weka.classifiers.functions.SMO", "-t", "testsData/labor.arff"),
        ("weka.classifiers.trees.J48", "-t", "testsData/weather.numeric.arff"),
        ("weka.classifiers.trees.J48", "-t", "testsData/weather.nominal.arff"),
        ("weka.classifiers.trees.DecisionStump", "-t", "testsData/cpu.with.vendor.arff"),  # @IgnorePep8
        ("weka.classifiers.trees.DecisionStump", "-t", "testsData/cpu.arff"),
        ("weka.classifiers.meta.AdaBoostM1", "-t", "testsData/breast-cancer.arff"),  # @IgnorePep8
        ("weka.classifiers.meta.AdaBoostM1", "-t", "testsData/labor.arff"),
        ("weka.classifiers.bayes.NaiveBayes", "-t", "testsData/credit-g.arff"),
        ("weka.classifiers.bayes.NaiveBayes", "-t", "testsData/iris.2D.arff")] #,
        #("weka.classifiers.functions.MultilayerPerceptron", "-t", "testsData/credit-g.arff"),  # @IgnorePep8
        #("weka.classifiers.functions.MultilayerPerceptron", "-t", "testsData/iris.2D.arff")  # @IgnorePep8
        #]

    questsList = []
    for ipNum in ipList:
        for touple in appTouples:
            questsList.append({
                "APPID": touple[0],
                "ARGS": touple[1],
                "DATA": touple[2],
                "PEER": ipNum
                })

    # Creates a new thread for each quest,
    # and commissions it by the quest handling function
    threadsArray = []
    resultsQueue = multiprocessing.Queue()
    for quest in questsList:
        process = multiprocessing.Process(target=handleQuest, args=(resultsQueue, quest,))  # @IgnorePep8
        threadsArray.append(process)
        process.start()

    print "\n\nJust sent the tests. Waiting.\n"

    # Waits for the answers, and prints them after time out
    time.sleep(TIME_WATCHDOG)
    results = [resultsQueue.get() for process in threadsArray]
    for resultsLine in results:
        print resultsLine
