#!/usr/bin/env python
import math
import subprocess
import time
import threading
import datetime
import sys

# Experiment Settings
# SCHEDULES = ['SCH_RNRO', 'SCH_FIFO', 'SCH_SJF']
SCHEDULES = ['SCH_RNRO', 'SCH_FIFO']
# SERVERS = [1, 4, 10]
SERVERS = [1]
# CLIENTS = [1, 4]
CLIENTS = [1, 2]

# System Settings
HEADER_CONFIG = 'CONFIG'
HEADER_RESET = 'RESET'
HEADER_SERVER_REST = 'SERVER_REST'
PORT_CONFIG = 21982
SCH_RNRO = SCHEDULES[0]
SCH_FIFO = SCHEDULES[1]
#SCH_SJF = SCHEDULES[2]


# Methods
def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n /= 10
    return s


def send2server(serverIP, message):
	proc = subprocess.Popen([
			"./sendMessage.sh",
			message,
			str(serverIP),
			str(PORT_CONFIG)
		], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
		universal_newlines=True)
	proc.wait()


def configureServer(serverIP, schedule, runnerName):
	send2server(serverIP, HEADER_RESET)
	time.sleep(0.25)
	send2server(serverIP,
		HEADER_CONFIG+" "+runnerName+" "+schedule)
	time.sleep(0.25)


def splitConfig(configur):
	config = str(configur)
	while (len(config) < 3): #4):
		config = '0'+config
	return int(config[0]), int(config[1]), int(config[2]) #, int(config[3])


def performRun(runnerName, configurs, time2run):
	serverList = []
	with open(runnerName+".serverlist", "r") as serverListFile:
		for serverIP in serverListFile:
			serverList.append(serverIP[:-1])
	for server in serverList:
		send2server(server, HEADER_CONFIG+" '-"+server+"-dummy-' "+SCH_RNRO)
	for config in configurs:
		RnRo, FiFo, nClients = splitConfig(config) # SJF, nClients = splitConfig(config)
		for server in serverList[0 : RnRo]:
			configureServer(server, SCH_RNRO, " '"+str(config)+"-"+server+"-"+runnerName+"-RNRO' "+SCH_RNRO)
		for server in serverList[RnRo : RnRo+FiFo]:
			configureServer(server, SCH_FIFO, " '"+str(config)+"-"+server+"-"+runnerName+"-FIFO' "+SCH_FIFO)
		# for server in serverList[RnRo+FiFo : RnRo+FiFo+SJF]:
		#	configureServer(server, SCH_SJF, " '"+str(config)+"-"+server+"-"+runnerName+"-SJF' "+SCH_SJF)
		print "\n"+runnerName+": Performing test configuration "+str(config)
		clientArgs = ''
		clients = []
		for server in serverList[0 : RnRo+FiFo]: # +SJF]:
			clientArgs += '-a '+server
		for numClient in range(0, nClients):
			clients.append(subprocess.Popen([
					"./runClient.sh",
					clientArgs
				], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
				universal_newlines=True))
		time.sleep(time2run)
	for server in serverList:
		send2server(server, HEADER_SERVER_REST)


if __name__=='__main__':
	time2run = int(sys.argv[1])
	configurations = []
	for comb in range(int(math.pow(10, len(SCHEDULES)+1))):
		for numClie in CLIENTS:
		    if comb % 10 == numClie:
		        for numServ in SERVERS:
		            if sum_digits(int(comb/10)) == numServ:
		                configurations.append(comb)
	testDuration = time2run*len(configurations)*1.05
	print "The tests have begun. Estimated test time: "+str(testDuration/60)+" minutes to run "+str(len(configurations))+" tests ("+str(time2run)+" seconds per test). Estimated time of test compleition: "+datetime.datetime.fromtimestamp(time.time()+testDuration).strftime('%Y-%m-%d %H:%M:%S')
	runner1 = threading.Thread(target=performRun, args=("Run1", configurations, time2run,))
	runner2 = threading.Thread(target=performRun, args=("Run2", configurations, time2run,))
	runner2.start()
	runner1.start()
