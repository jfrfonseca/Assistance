#!/usr/bin/env python
import math
import subprocess
import time
import threading
import datetime
import sys

# Experiment Settings
SCHEDULES = ['SCH_RNRO', 'SCH_FIFO', 'SCH_SJF']
SERVERS = [1]
CLIENTS = [1]

# System Settings
HEADER_CONFIG = 'CONFIG'
HEADER_RESET = 'RESET'
HEADER_SERVER_REST = 'SERVER_REST'
PORT_CONFIG = 21982
SCH_RNRO = SCHEDULES[0]
SCH_FIFO = SCHEDULES[1]
SCH_SJF = SCHEDULES[2]


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
	while (len(config) < 4):
		config = '0'+config
	return int(config[0]), int(config[1]), int(config[2]), int(config[3])


if __name__=='__main__':
	# Get Args
	time2run = int(sys.argv[1])
	runnerName = str(sys.argv[2])
	# Form possible configurations
	configurations = []
	for comb in range(int(math.pow(10, len(SCHEDULES)+1))):
		for numClie in CLIENTS:
		    if comb % 10 == numClie:
		        for numServ in SERVERS:
		            if sum_digits(int(comb/10)) == numServ:
		                configurations.append(comb)
	# Inform the user
	testDuration = time2run*len(configurations)*1.05
	print "The tests have begun. Estimated test time: "+str(testDuration/60)+" minutes to run "+str(len(configurations))+" tests ("+str(time2run*1.05)+" seconds per test). Estimated time of test compleition: "+datetime.datetime.fromtimestamp(time.time()+testDuration).strftime('%Y-%m-%d %H:%M:%S')
	# Prepares the servers
	serverList = []
	with open(runnerName+".serverlist", "r") as serverListFile:
		for serverIP in serverListFile:
			serverList.append(serverIP.replace("\n", ""))
	print "\n"+runnerName+": Servers: "+str(serverList)
	for server in serverList:
		send2server(server, HEADER_CONFIG+" '-"+server+"-dummy-' "+SCH_RNRO)
	# For each configuration
	for config in configurations:
		# Configures the servers
		RnRo, FiFo, SJF, nClients = splitConfig(config)
		for server in serverList[0 : RnRo]:
			configureServer(server, SCH_RNRO, " '"+str(config)+"-"+server+"-"+runnerName+"-RNRO' "+SCH_RNRO)
		for server in serverList[RnRo : RnRo+FiFo]:
			configureServer(server, SCH_FIFO, " '"+str(config)+"-"+server+"-"+runnerName+"-FIFO' "+SCH_FIFO)
		for server in serverList[RnRo+FiFo : RnRo+FiFo+SJF]:
			configureServer(server, SCH_SJF, " '"+str(config)+"-"+server+"-"+runnerName+"-SJF' "+SCH_SJF)
		# Configures the Client
		clientArgs = ''
		clients = []
		for server in serverList[0 : RnRo+FiFo+SJF]:
			clientArgs += ' -a '+server
		# Calls each client
		print "\n"+runnerName+": Performing test configuration "+str(config)+" on servers '"+clientArgs+"', until "+datetime.datetime.fromtimestamp(time.time()+(time2run*1.05)).strftime('%Y-%m-%d %H:%M:%S')
		for numClient in range(0, nClients):
			clients.append(subprocess.Popen([
					"./runClient.sh",
					clientArgs
				], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
				universal_newlines=True))
		# Waits compleition
		time.sleep(time2run*1.05)
		# End LOOP
	# Rests the Servers
	for server in serverList:
		send2server(server, HEADER_SERVER_REST)
