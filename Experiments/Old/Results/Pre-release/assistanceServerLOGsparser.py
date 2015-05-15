#!/usr/bin/env python
'''
Prints a more analisys-friendly version of the assistance experiments in the current folder
Jose F. R. Fonseca
See Attached License file
'''
import os

def filesNames(lineOfFiles):
    names = []
    if lineOfFiles.find(',') != -1:
        filesArray = lineOfFiles.split[',']
        for filepath in filesArray:
            names.append(filepath.split('/')[-1])
            if names[-1].find('[') != -1:
                names[-1].replace("]", "").replace("[", "").replace("'", "")
    else:
        names.append(lineOfFiles.split('/')[-1])
        if names[-1].find('[') != -1:
            names[-1].replace("]", "").replace("[", "").replace("'", "")
    return names

def parseOneQuestLOG_natural(blockString):
    '''
    Returns a Dictionary with the LOG register contents
    '''
    # print blockString
    dict = {}
    # breaks into lines
    arrayBlockString = []
    arrayBlockString = blockString.splitlines()
    #print arrayBlockString
    arrayBlockString = arrayBlockString[1:]
    #print arrayBlockString
    
    if len(arrayBlockString) > 23 and arrayBlockString[4] in ["SHA256_TEST", "WEKA_3_6_12"]:
        # checks if error
        if arrayBlockString[0] != "<BEGIN>":
            raise ValueError("LOG REGISTER ERROR! LOG REGISTER:\n========\n"+arrayBlockString[0]+"\n========\n")
        # if not error,
        dict['TICKET'] = arrayBlockString[1]
        dict['TIME_RECEIVED'] = float(arrayBlockString[3]) 
        dict['APPID'] = arrayBlockString[4] 
        dict['ARGS'] = arrayBlockString[5]
        dict['DATA_FILES_NAMES'] = filesNames(arrayBlockString[6])
        # time of completed local - time of performing local
        dict['TIMEOF_PROCESSING'] = float(arrayBlockString[21][:13]) - float(arrayBlockString[20][:13])
        dict['CPU_ON_BEGIN'] = float(arrayBlockString[16].split('CPU=')[1].split('mem')[0])
        dict['MEM_ON_BEGIN'] = float(arrayBlockString[16].split("cal': ")[1].split('}')[0])
        # Time completed - time received
        dict['TIMEOF_COMPLETION'] = float(arrayBlockString[9]) - float(arrayBlockString[3]) 
        # time of data gathering - time of sys analisys + time of data sent - time of task ready
        dict['TIMEOF_WAITING_CLIENT'] = (float(arrayBlockString[17][:13]) - float(arrayBlockString[16][:13]))\
                                                            + (float(arrayBlockString[23][:13]) - float(arrayBlockString[22][:13]))
        # time of sys analysis - time of draft + time of start performance - time of data ready
        dict['TIMEOF_WAITING_SERVER'] = (float(arrayBlockString[16][:13]) - float(arrayBlockString[15][:13]))\
                                                            + (float(arrayBlockString[20][:13]) - float(arrayBlockString[18][:13]))
        # dict['SCRIPT_ARRAY'] = ast.literal_eval(arrayBlockString[7])
        dict['ANSWER_FILES_NAMES'] = filesNames(arrayBlockString[11])
        for file in filesNames(arrayBlockString[12]):
            dict['ANSWER_FILES_NAMES'].append(file)
        # time of data ready - time of data gathering
        dict['TIMEOF_DATA_TRANSFER'] = float(arrayBlockString[18][:13]) - float(arrayBlockString[17][:13])
        # time of finished - time of sending data
        dict['TIMEOF_ANSWER_TRANSFER'] = float(arrayBlockString[24][:13]) - float(arrayBlockString[23][:13])
    return dict


def sumFiles(filesList):
    total = 0
    for filename in filesList:
        total += len(open(filename, 'rb').read())
    return total


def printLog():
    headerString = "EXPERIMENT;INSTANCE_TYPE;HOST_IP;RUN_TYPE;TICKET;TIME_RECEIVED;"\
    +"APP_ID;ARGUMENTS;COMPLEITION_TIME;DATA_TRANSFER_TIME;DATA_SIZE;DATA_FILES;ANSWER_TRANSFER_TIME;ANSWER_SIZE;"\
    +"WAITING_CLIENT_TIME;WAITING_SERVER_TIME;PROCESSING_TIME;CPU_PERCENT;MEM_PERCENT;TIME()_REAL;TIME()_USER;TIME()_SYS;"
    with open("serverLOGs.csv", 'w') as outputFile:
        outputFile.write(headerString+'\n')
        experimentsList = []
        for experiment in (next(os.walk('.'))[1]):
            if experiment.split(' ')[0] == 'AssistanceExperiment':
                for instanceType in ['Client', 'Server']:
                    for hostDir in (next(os.walk(experiment+'/'+instanceType))[1]):
                        for logsDir in (next(os.walk(experiment+'/'+instanceType+'/'+hostDir))[1]):
                            ticketWD = lambda ticket : experiment+'/'+instanceType+'/'+hostDir+'/'+logsDir+"/AssistanceApps/runtimeIO/"+ticket+"/"
                            logFile = open(experiment+'/'+instanceType+'/'+hostDir+'/'+logsDir+'/LOG/officerLogFile.log', 'r')
                            data = logFile.read()
                            logs = data.split('<END>')
                            for register in logs[:-1]:
                                dict = parseOneQuestLOG_natural(register)
                                if len(dict) > 0:
                                    datafilesList = os.listdir(ticketWD(dict['TICKET']))
                                    dataList = []
                                    namesList = []
                                    for fileIndex in range(len(datafilesList)):
                                        if datafilesList[fileIndex].find(dict['TICKET']) == -1:
                                            dataList.append(ticketWD(dict['TICKET'])+datafilesList[fileIndex])
                                            namesList.append(datafilesList[fileIndex])
                                    namesString = ''
                                    for name in namesList:
                                        namesString += name+" "
                                    line = experiment.split(' ')[1] + ';' + instanceType + ';'\
                                        + hostDir + ';'\
                                        + logsDir.split('-')[-1] + ';'\
                                        + dict['TICKET'] + ';'\
                                        + str(dict['TIME_RECEIVED'])  + ';'\
                                        + dict['APPID'] + ';' + dict['ARGS'] + ';'\
                                        + str(dict['TIMEOF_COMPLETION']) + ';'\
                                        + str(dict['TIMEOF_DATA_TRANSFER']) + ';' + str(sumFiles(dataList)) + ';' + namesString + ';'\
                                        + str(dict['TIMEOF_ANSWER_TRANSFER']) + ';'\
                                        + str(sumFiles([ticketWD(dict['TICKET'])+dict['TICKET']+"-"+"stdout.dat",
                                                        ticketWD(dict['TICKET'])+dict['TICKET']+"-"+"stderr.dat"])) + ';'\
                                        + str(dict['TIMEOF_WAITING_CLIENT']) + ';' + str(dict['TIMEOF_WAITING_SERVER']) + ';'\
                                        + str(dict['TIMEOF_PROCESSING']) + ';'\
                                        + str(dict['CPU_ON_BEGIN']) + ';' + str(dict['MEM_ON_BEGIN']) + ';'
                                    for timeLine in (open(ticketWD(dict['TICKET'])+dict['TICKET']+"-"+"stderr.dat", 'r').read()).splitlines():
                                        line += timeLine.split(' ')[1] + ';'
                                    outputFile.write(line+'\n')
'''
Runs this file
'''
if __name__ == '__main__':
    printLog()