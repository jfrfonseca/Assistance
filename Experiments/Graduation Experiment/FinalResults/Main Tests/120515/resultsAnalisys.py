#!/usr/bin/env python
import sqlite3

'''results (configuration text, run text, serverIP text, scheduling text, appTouple text, response real, transfer real, execution real)'''

AVERAGE_TIME_PER_QUEST_DESC = "AVERAGE RESPONSE, PROCESSING TIME PER CONFIGURATION, SCHEDULE STRATEGY, QUEST:"
AVERAGE_TIME_PER_QUEST_QUERY = '''select serverIP, configuration, scheduling, appTouple, avg(response), avg(execution) from results group by serverIP, configuration, scheduling, appTouple'''

AVERAGE_TIME_PER_APP_DESC = "AVERAGE RESPONSE, PROCESSING TIME PER APP TOUPLE:"
AVERAGE_TIME_PER_APP_QUERY = '''select appTouple, avg(response), avg(execution)  from results group by appTouple'''

AVERAGE_TIME_PER_APP_PER_SCH_DESC = "AVERAGE RESPONSE, PROCESSING TIME PER APP TOUPLE PER SCHEDULE STRATEGY:"
AVERAGE_TIME_PER_APP_PER_SCH_QUERY = '''select appTouple, scheduling, avg(response), avg(execution) from results group by appTouple, scheduling'''

TOTAL_TIME_PER_CONF_DESC = "AVERAGE TOTAL RESPONSE, PROCESSING TIME PER CONFIGURATION:"
TOTAL_TIME_PER_CONF_QUERY = '''select configuration, avg(rsp), avg(exe) from (
select configuration, run, sum(response) as rsp, sum(execution) as exe from results group by configuration, run
) group by configuration'''

RESPyPRO_PER_CONF_DESC = "AVERAGE RESPONSE/PROCESSING TIME PER CONFIGURATION:"
RESPyPRO_PER_CONF_QUERY = '''select configuration, (avg(rsp)/avg(exe)) from (
select configuration, run, sum(response) as rsp, sum(execution) as exe from results group by configuration, run
) group by configuration'''

RESPyPRO_PER_CONF_SCH_DESC = "AVERAGE RESPONSE/PROCESSING TIME PER SCHEDULE STRATEGY, CONFIGURATION:"
RESPyPRO_PER_CONF_SCH_QUERY = '''select configuration, scheduling, (avg(rsp)/avg(exe)) from (
select configuration, scheduling, run, sum(response) as rsp, sum(execution) as exe from results group by configuration, scheduling, run
) group by configuration, scheduling'''

RESPyPRO_PER_SCH_DESC = "AVERAGE RESPONSE/PROCESSING TIME PER SCHEDULE STRATEGY:"
RESPyPRO_PER_SCH_QUERY = '''select scheduling, (avg(rsp)/avg(exe)) from (
select scheduling, run, sum(response) as rsp, sum(execution) as exe from results group by scheduling, run
) group by scheduling'''

AVERAGE_TIME_PER_SERV_CONF_SCH_DESC = "AVERAGE RESPONSE, PROCESSING TIME PER SERVER, CONFIGURATION, SCHEDULE STRATEGY ON SERVER:"
AVERAGE_TIME_PER_SERV_CONF_SCH_QUERY = '''select serverIP, configuration, scheduling, avg(response), avg(execution) from results group by serverIP, configuration, scheduling'''

namesList = [AVERAGE_TIME_PER_QUEST_DESC,
             AVERAGE_TIME_PER_APP_DESC,
             AVERAGE_TIME_PER_APP_PER_SCH_DESC,
             TOTAL_TIME_PER_CONF_DESC,
             RESPyPRO_PER_CONF_DESC,
             RESPyPRO_PER_CONF_SCH_DESC,
             RESPyPRO_PER_SCH_DESC,
             AVERAGE_TIME_PER_SERV_CONF_SCH_DESC]

analisysList = [AVERAGE_TIME_PER_QUEST_QUERY,
                AVERAGE_TIME_PER_APP_QUERY,
                AVERAGE_TIME_PER_APP_PER_SCH_QUERY,
                TOTAL_TIME_PER_CONF_QUERY,
                RESPyPRO_PER_CONF_QUERY,
                RESPyPRO_PER_CONF_SCH_QUERY,
                RESPyPRO_PER_SCH_QUERY,
                AVERAGE_TIME_PER_SERV_CONF_SCH_QUERY]


if __name__ == '__main__':
    db = sqlite3.connect('experimentResults')
    c = db.cursor()
    for index, analisys in enumerate(analisysList):
        print "<BEGIN>"
        print namesList[index]
        c.execute(analisys)
        results = c.fetchall()
        for line in results:
            print line
        print "<END>"
    db.close()
