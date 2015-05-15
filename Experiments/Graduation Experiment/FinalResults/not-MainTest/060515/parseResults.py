if __name__ == '__main__':
	total = 0
	with open("times.txt", "r") as timesFile:
		linesStr = timesFile.read()
		lines = linesStr.splitlines()
		for offset in [ofst for ofst in range(0,35) if ((ofst%3) == 0)]:
			timeReal = float(lines[offset].split(" ")[1])
			for timeRealLine in [line for line in range(offset+1,len(lines)) if ((line-offset)%36) == 0]:
				# print str(timeRealLine)+"="+lines[timeRealLine].split(" ")[1]
				timeReal = (timeReal+float(lines[timeRealLine].split(" ")[1]))/2
			print "AVG="+str(timeReal)
			total += timeReal
	print "TOTAL="+str(total)

'''
Results for Baseline Performance Weka:
RaiseFree - 5 runs:
AVG=1.49375
AVG=1.03125
AVG=0.36625
AVG=0.330625
AVG=0.633125
AVG=0.63375
AVG=1.031875
AVG=1.02125
AVG=1.18125
AVG=0.5175
AVG=295.86
AVG=2.04125
TOTAL=306.141875
'''
