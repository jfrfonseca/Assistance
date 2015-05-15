#!/usr/bin/env python
import sqlite3
import os
import sys


'''results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)'''


if __name__ == '__main__':
	alldb = sqlite3.connect('allResults')
	allCursor = alldb.cursor()
	allCursor.execute("CREATE TABLE results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)")
	for dayExperiment in (next(os.walk('./'))[1]):
		allCursor.execute("attach '"+dayExperiment+"/experimentResults' as merged;")
		allCursor.execute("insert into results select * from merged.results;")
		allCursor.execute("detach database merged;")

	if len(sys.argv) > 1 and sys.argv[1] == "--print":
		allCursor.execute("select * from results")
		results = allCursor.fetchall()
		# Sorts the results list per configuration
		sorted(results, key=lambda x: int(x[0]))
		print "<BEGIN>"
		print '''results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)'''
		for line in results:
			print line
		print "<END>"

	alldb.close()