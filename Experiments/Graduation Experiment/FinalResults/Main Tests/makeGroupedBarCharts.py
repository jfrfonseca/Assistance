#!/usr/bin/env python
import sqlite3
import os
import sys
import math
import plotly.plotly as py
from plotly.graph_objs import *


'''results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)'''

def sqliteLog(val):
    return math.log(val)


def sqliteExp(val):
    return math.exp(val)


def sumDigits(conf):
    config = int(conf)/10
    total = 0
    while config >= 1:
        total += config % 10
        config /= 10
    return total


def colIndexesOfConf(numColumns, conf, results):
    response = []
    # Normalizes the length of the configuration:
    config = str(conf)
    while len(config) < 4:
        config = "0"+config
    # Gets to the configuration's first line in the results (that are sorted by configuration, schedule)
    for lineNum, line in enumerate(results):
        if line[0] == str(conf):
            break
    # For each schedule and qtd of servers in this schedule
    for schedTpl in [("RNRO", int(config[0]), ), ("FIFO", int(config[1]), ), ("SJF", int(config[2]), )]:
        offset = 0
        numAdded = 0
        while numAdded < schedTpl[1]:
            if results[lineNum+offset][1] == schedTpl[0]:
                response.append(lineNum+offset)
                numAdded += 1
            offset += 1
    print len(response) == 4
    return response


def calculateGeoMean(dataList):
    somatory = 0
    for dat in dataList:
        somatory += math.log(dat)
    return math.exp(somatory/len(dataList))


greekAlphabet = ["ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON", "ZETA",
				"ETA", "THETA", "IOTA", "KAPPA", "LAMBDA", "MU",
				"NU", "XI", "OMICRON", "PI", "RHO", "SIGMA",
				"TAU", "UPSILON", "PHI", "CHI", "PSI", "OMEGA"]


if __name__ == '__main__':
    
    QUERY = "select configuration, scheduling, serverIP, exp(avg(log(response))), exp(avg(log(execution))) from ("\
                        +"select configuration, scheduling, serverIP, response, execution, run"\
                                +" from results group by configuration, scheduling, serverIP, run"\
                    +") group by configuration, scheduling, serverIP"
    
    alldb = sqlite3.connect('allResults')
    alldb.create_function("log", 1, sqliteLog)
    alldb.create_function("exp", 1, sqliteExp)
    allCursor = alldb.cursor()

    # Settings for this reading
    numServers = 4
    numClients = 1

    # Gets the results wanted
        # Gets the lines of the DatSet
    queryResults = []
    allCursor.execute(QUERY)
    queryResults = allCursor.fetchall()
    alldb.close()
    allResults = sorted(queryResults, key=lambda x: 10*int(x[0])+int(["RNRO", "FIFO", "SJF"].index(x[1])))        
        # Separated the results wanted
    results = []
    for line in allResults:
        if sumDigits(line[0]) == numServers and int(line[0]) % 10 == numClients:
            results.append(line)
    
    # Gets the number of configurations
    allConfigurations = sorted(list(set([lin[0] for lin in results])), key=lambda x: int(x))
    numConfigurations = len(allConfigurations)

    # Creates the output structure
    allGroupsResp = []
    allGroupsProc = []
    for grp in range(numServers):
        allGroupsResp.append([])
        allGroupsProc.append([])

    # Gets the results for each configuration
    for conf in allConfigurations:
        offset = colIndexesOfConf(numServers, conf, results)
        for col in range(numServers):
            print results[offset[col]]
            allGroupsResp[col].append(results[offset[col]][3])
            allGroupsProc[col].append(results[offset[col]][4])

    # Make Grouped Bar Charts of time of execution per configuration, per server - qtdServers, 1 Client
    xNamesList = ["Conf. "+config for config in allConfigurations]
    # Response time:
    data2graph = []
    title =  "Total Response time per Configuration, Per Server - "+str(numServers)+" Servers, 1 Client"
        # Make the Data:
    for grpIndex, group in enumerate(allGroupsResp):
        data2graph.append(
                          Bar(
                              x=xNamesList,
                              y=group,
                              name="Response time for Server "+greekAlphabet[grpIndex]
                              )
                          )
		# Get the GeoMean of the data for each configuration
    geoMeanOfConf = lambda confIndex, timeTypeGroups: calculateGeoMean([group[confIndex] for group in timeTypeGroups])
    geoMeansGroup = lambda timeTypeGroups: [geoMeanOfConf(confIndex, timeTypeGroups) for confIndex, conf in enumerate(allConfigurations)]
    data2graph.append(
                      Bar(
                          x=xNamesList,
                          y=geoMeansGroup(allGroupsResp),
                          name="Geometric Mean of Configuration"
                          )
                      )
        # Perform the plotting
    plot_utl = py.plot(Figure(data=data2graph, layout=Layout(barmode='group')), filename=title)
    # Processing time:
    data2graph = []
    title =  "Total Processing time per Configuration, Per Server - "+str(numServers)+" Servers, 1 Client"
        # Make the Data:
    for grpIndex, group in enumerate(allGroupsProc):
        data2graph.append(
                          Bar(
                              x=xNamesList,
                              y=group,
                              name="Processing time for Server "+greekAlphabet[grpIndex]
                              )
                          )
    data2graph.append(
                      Bar(
                          x=xNamesList,
                          y=geoMeansGroup(allGroupsProc),
                          name="Geometric Mean of Configuration"
                          )
                      )
        # Perform the plotting
    plot_utl = py.plot(Figure(data=data2graph, layout=Layout(barmode='group')), filename=title)
