#!/usr/bin/env python
'''
Prints a more analisys-friendly version of the assistance experiments in the current folder
Each line of the logs has:
Jose F. R. Fonseca
See Attached License file
'''
EXPERIMENT = 0
INSTANCE_TYPE = 1
HOST_IP = 2
RUN_TYPE = 3
TICKET = 4
TIME_RECEIVED = 5
APP_ID = 6
ARGUMENTS = 7
COMPLEITION_TIME = 8
DATA_TRANSFER_TIME = 9
DATA_SIZE = 10
DATA_FILES = 11
ANSWER_TRANSFER_TIME = 12
ANSWER_SIZE = 13
WAITING_CLIENT_TIME = 14
WAITING_SERVER_TIME = 15
PROCESSING_TIME = 16
CPU_PERCENT = 17
MEM_PERCENT = 18
TIME_REAL = 19
TIME_USER = 20
TIME_SYS = 21



def updateByRun(runs, data):
    if runs.has_key(data[RUN_TYPE]):
        metrics = runs[data[RUN_TYPE]]
        metrics["responseTime"] = (float(data[COMPLEITION_TIME]) + metrics["responseTime"]) / 2
        metrics["transferTime"] = ((float(data[DATA_TRANSFER_TIME]) + float(data[ANSWER_TRANSFER_TIME])) + metrics["transferTime"]) / 2
        metrics["executionTime"] = (float(data[TIME_REAL]) + metrics["executionTime"]) / 2
    else:
        metrics = {}
        metrics["responseTime"] = float(data[COMPLEITION_TIME])
        metrics["transferTime"] = float(data[DATA_TRANSFER_TIME]) + float(data[ANSWER_TRANSFER_TIME])
        metrics["executionTime"] = float(data[TIME_REAL])
    return metrics


def averageByRun(runs):
    metrics = {}
    for run in runs.keys():
        if run != "Baseline":
            if len(metrics.keys()) == 0:
                metrics = runs[run]
            else:
                metrics["responseTime"] = (metrics["responseTime"] + runs[run]["responseTime"]) / 2
                metrics["transferTime"] = (metrics["transferTime"] + runs[run]["transferTime"]) / 2
                metrics["executionTime"] = (metrics["executionTime"] + runs[run]["executionTime"]) / 2
    return metrics


def getStats():
    with open("serverLOGs.csv", 'r') as logsFile:
        logsFile.readline()
        appTouples = {}

        while True:
            try:
                line = logsFile.readline()
                data = line.split(';')[:-1]
                touple = data[EXPERIMENT]+";"+data[APP_ID]+";"+data[ARGUMENTS]+";"+data[DATA_FILES]
                if appTouples.has_key(touple):
                    appTouples[touple][data[RUN_TYPE]] = updateByRun(appTouples[touple], data)
                else:
                    appTouples[touple] = {}
                    appTouples[touple][data[RUN_TYPE]] = updateByRun({}, data)
            except IndexError:
                break
        # Runs Average
        # print appTouples
        for app in appTouples.keys():
            appTouples[app]["Average"] = averageByRun(appTouples[app])
        # Printout
        with open("serverLOGanalisys.csv", 'w') as outputFile:
            outputFile.write("EXPERIMENT;APPID;ARGUMENTS;DATA_FILES;RESPONSE_TIME;TRANSFER_TIME;EXECUTION_TIME;\n")
            for app in appTouples.keys():
                outString = app+";"
                for item in ["responseTime", "transferTime", "executionTime"]:
                    outString += str(appTouples[app]["Average"][item])+';'
                outputFile.write(outString+'\n')

     
'''
Runs this file
'''
if __name__ == '__main__':
    getStats()