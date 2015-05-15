#!/usr/bin/env python
import sqlite3
import os
import sys
import math
import plotly.plotly as py
from plotly.graph_objs import *


'''results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)'''

AVERAGE_TIME_PER_CONF_SCH_QUERY = '''select configuration, scheduling, exp(avg(log(rsp))), exp(avg(log(exe))) from ('''\
                                                                    +'''select run, configuration, scheduling, sum(response) as rsp, sum(execution) as exe'''\
                                                                            +''' from results group by configuration, scheduling, run'''\
                                                                +''') group by configuration, scheduling'''

analisysList = [AVERAGE_TIME_PER_CONF_SCH_QUERY]


def sumDigits(conf):
    config = int(conf)/10
    total = 0
    while config >= 1:
        total += config % 10
        config /= 10
    return total


def getYvalues(xNamesList, results):
    # Gets the Y axis values
    rnroRespTimes = []
    rnroProcTimes = []
    fifoRespTimes = []
    fifoProcTimes = []
    sjfRespTimes = []
    sjfProcTimes = []
    # For each configuration
    for index, conf in enumerate(xNamesList):
        # scheOnServer, response, execution
        times = [(lin[1], lin[2], lin[3]) for lin in results if lin[0] == conf]
        timesDict = {}
        for itm in times:
            # The values for each schedule
            timesDict[itm[0]] = (itm[1], itm[2])
        if "RNRO" in [conf[0] for conf in times]:
            rnroRespTimes.append(float(timesDict["RNRO"][0]))
            rnroProcTimes.append(float(timesDict["RNRO"][1]))
        else:
            rnroRespTimes.append(0)
            rnroProcTimes.append(0)
        if "FIFO" in [conf[0] for conf in times]:
            fifoRespTimes.append(float(timesDict["FIFO"][0]))
            fifoProcTimes.append(float(timesDict["FIFO"][1]))
        else:
            fifoRespTimes.append(0)
            fifoProcTimes.append(0)
        if "SJF" in [conf[0] for conf in times]:
            sjfRespTimes.append(float(timesDict["SJF"][0]))
            sjfProcTimes.append(float(timesDict["SJF"][1]))
        else:
            sjfRespTimes.append(0)
            sjfProcTimes.append(0)
    return rnroRespTimes, rnroProcTimes, fifoRespTimes, fifoProcTimes, sjfRespTimes, sjfProcTimes


def sqliteLog(val):
    return math.log(val)


def sqliteExp(val):
    return math.exp(val)


def makeStackGraph(text_xNamesList, dataDict):
    data2graph = []
    for dataTouple in dataDict["dataList"]:
        data2graph.append(
                          Bar(
                              x=text_xNamesList,
                              y=dataTouple[1],
                              name=dataTouple[0]
                              )
                          )
    return py.plot(Figure(data=data2graph, layout=Layout(barmode='stack')), filename=dataDict["title"])


if __name__ == '__main__':
    alldb = sqlite3.connect('allResults')
    alldb.create_function("log", 1, sqliteLog)
    alldb.create_function("exp", 1, sqliteExp)
    allCursor = alldb.cursor()
    
    for index, analisys in enumerate(analisysList):
        allCursor.execute(analisys)
        results = allCursor.fetchall()
    # Sorts the results list per configuration
    sorted(results, key=lambda x: int(x[0]))
    
    for qtdServers in [4, 9]:
        # Stacked Bar Charts of time of execution per configuration, per scheduling - qtdServers, 1 Client
        xNamesList = sorted(list(set([str(config[0]) for config in results if str(config[0])[-1] == "1" and sumDigits(str(config[0])) == qtdServers])), key=lambda x: int(x))
        rnroRespTimes, rnroProcTimes, fifoRespTimes, fifoProcTimes, sjfRespTimes, sjfProcTimes = getYvalues(xNamesList, results)
        # data to plot
        graphResponse = {
                  "title": "Total Response time per Configuration, time spent on each Type of Server - "+str(qtdServers)+" Servers, 1 Client",
                  "dataList": [("Response Time RNRO", rnroRespTimes, ), ("Response Time FIFO", fifoRespTimes, ), ("Response Time SJF", sjfRespTimes, )]
                }
        
        graphProcessing = {
                  "title": "Total Processing time per Configuration, time spent on each Type of Server - "+str(qtdServers)+" Servers, 1 Client",
                  "dataList": [("Processing Time RNRO", rnroProcTimes, ), ("Processing Time FIFO", fifoProcTimes, ), ("Processing Time SJF", sjfProcTimes, )]
                }
        # Perform the plotting
        plot_utl = makeStackGraph(["Conf. "+config for config in xNamesList], graphResponse)
        plot_utl = makeStackGraph(["Conf. "+config for config in xNamesList], graphProcessing)

    alldb.close()