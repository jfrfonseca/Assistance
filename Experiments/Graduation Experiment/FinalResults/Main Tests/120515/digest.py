#!/usr/bin/env python
import sqlite3
import ast
import os

# Constants
BASEDIR = "Results"


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


def parse_Config_ServerName_Run_Type(folderName):
	namePieces = (folderName.split("'")[1]).split("-")
	return namePieces[0], namePieces[1], namePieces[2], namePieces[3]


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
	for serverFolder in (next(os.walk('RunO/'))[1]):
		include = []
		config, serverIP, run, serverType = parse_Config_ServerName_Run_Type(serverFolder)
		with open('RunO/'+serverFolder+"/LOG/officerLogFile.log", 'r') as logFile:
			for logChunk in splitLog(logFile.read()):
				try:
					response, transfer, execution = getValues('RunO/'+serverFolder, logChunk)
					insert = (config, run, serverIP, serverType, appTouple2string(logChunk), response, transfer, execution, )
					include.append(insert)
				except IOError:
					pass
			c.executemany("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?)", include)
			db.commit()
	#c.execute(TEST1)
	#results = c.fetchall()
	#for line in results:
	#	print line
	db.close()
