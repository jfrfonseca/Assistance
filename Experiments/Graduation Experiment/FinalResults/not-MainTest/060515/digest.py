#!/usr/bin/env python
import sqlite3
import ast
import os

# Constants
BASEDIR = "Results"
EXP_CONF = ["041", "131", "221", "311", "401"]
NUM_RUNS = 1


# analisys queries
CREATE_TABLE = '''CREATE TABLE results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)'''
TEST1 = '''select * from results'''


# Lines of certain data in LOG chunks
TIME_RECEIVED = 3
APP_ID = 4
ARGS = 5
DATA_FILES = 6
TIME_FINISHED = 9
STDERR = 12
GATHERING = 17
DATA_READY = 18
SENDING_DATA = 23


def parseServerNameType(folderName):
	namePieces = folderName.split("-")
	servType = (namePieces[3].split("_"))[1]
	if servType == 'NONE':
		servType = 'RndRob'
	return namePieces[1], servType


def appTouple2string(logChunk):
	answer = logChunk[APP_ID]+":::"+logChunk[ARGS]
	filesList = ast.literal_eval(logChunk[DATA_FILES])
	for fileName in filesList:
		answer += ":::"+fileName.split('/')[-1]
	return answer


def splitLog(fullLog):
	ans = []
	rawChunks = fullLog.split("<END>")[:-1]
	for rawPiece in rawChunks:
		piece = rawPiece.split("<BEGIN>")[1]
		pieceLines = piece.splitlines()
		ans.append(pieceLines)
	return ans


def getValues(directory, logChunk):
	response = float(logChunk[TIME_FINISHED].split("\t")[0]) - float(logChunk[TIME_RECEIVED].split("\t")[0])
	transfer = float(logChunk[DATA_READY].split("\t")[0]) - float(logChunk[GATHERING].split("\t")[0])
	with open(directory+'/'+logChunk[STDERR], 'r') as timeFile:
		lines = (timeFile.read()).splitlines()
		execution = float(lines[0].split(" ")[1])
	return response, transfer, execution


if __name__ == '__main__':
	db = sqlite3.connect('experimentResults')
	c = db.cursor()
	# Create table
	c.execute(CREATE_TABLE)
	for expConf in EXP_CONF:
		for runNumber in range(1, NUM_RUNS+1):
	 		for serverFolder in (next(os.walk(
										BASEDIR+'/'
										+expConf+'/'
										+"Run"+str(runNumber)))[1]):
				include = []
				serverIP, serverType = parseServerNameType(serverFolder)
				with open(BASEDIR+'/'
						+expConf+'/'
						+"Run"+str(runNumber)+'/'
						+serverFolder+'/'
						+"LOG/officerLogFile.log", 'r') as logFile:
					for logChunk in splitLog(logFile.read()):
						response, transfer, execution = getValues(BASEDIR+'/'+expConf+'/'+"Run"+str(runNumber)+'/'+serverFolder, logChunk)
						insert = (expConf, "Run"+str(runNumber), serverIP, serverType, appTouple2string(logChunk), response, transfer, execution, )
						include.append(insert)
				c.executemany("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?)", include)
				db.commit()
	c.execute(TEST1)
	results = c.fetchall()
	for line in results:
		print line
	db.close()
