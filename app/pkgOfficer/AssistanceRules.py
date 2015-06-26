#!/usr/bin/env python
'''
AssistanceDBMS.py - Returns data to the Assisance System runtime
from the data warehouse facility
Jose F. R. Fonseca
See Attached License file
'''
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import\
    AppID_LOCAL_ECHO_TEST, AppID_SHA256_TEST, AppID_SHA256_REMOTE_TEST,\
    NULL, DIR_APPS_CWD, TUNNING_DEFAULT_PROCESS_PRIORITY, AppID_WEKA,\
    SCHEDULE_SJF, SCHEDULE_FIFO, SCHEDULE_FIFO_MAX_PARALLEL_TASKS,\
    SCHEDULE_ROUNDROBIN, SCHEDULE_SJF_MAX_PARALLEL_TASKS, AppID_GPP, AppID_GCC


def stringfy(myList, mySeparator):
    if len(myList) > 0:
        myOutput = myList[0]
        if len(myList) > 1:
            for myItem in myList[1:]:
                myOutput += mySeparator+myItem
        return myOutput
    else:
        return ''


def volunteer(taskDescription):  # @UnusedVariable
    '''
    Decides if a task will be performed locally
    :param taskDescription:
    '''
    return True


def getCallerScript(taskDescription):
    '''
    Forms the script to run the given task
ALL ARGUMENTS COME AS A STRING - the data they refer may differ.
EVERY ASSISTANCEAPP MUST HAVE A DEFAULT DATA FILES (DATA AND ANSWER)
FOLDER, AND THIS FOLDER WILL DE SUBSCRIBED IN THE DBMS FOR EACH APP,
SO THE APP CAN CALL ITS FILES FROM THE DEFAULT
    :param taskDescription: the task to be analyzed
    '''
    args = taskDescription.ARGUMENTS
    if args == NULL:
        args = ""
    scriptSettings = {}
    scriptSettings["processPriority"] = str(taskDescription.PROCESS_PRIORITY)
    scriptSettings["dataFiles"] = stringfy(taskDescription.DATA_FILES, ' ')
    scriptSettings["TICKET"] = taskDescription.TICKET
    scriptSettings["args"] = args
    if taskDescription.APPID == AppID_LOCAL_ECHO_TEST:
        scriptSettings["assistanceAppFile"] = "echoInAllCaps.assistanceApp"
    elif taskDescription.APPID == AppID_SHA256_TEST:
        scriptSettings["assistanceAppFile"] = "sha256Example.assistanceApp"
    elif taskDescription.APPID == AppID_SHA256_REMOTE_TEST:
        scriptSettings["assistanceAppFile"] = "sha256Example.assistanceApp"
    elif taskDescription.APPID == AppID_WEKA:
        scriptSettings["assistanceAppFile"] = "assistanceWEKA.assistanceApp"
    elif taskDescription.APPID == AppID_GPP:
        scriptSettings["assistanceAppFile"] = "assistanceGpp.assistanceApp"
    elif taskDescription.APPID == AppID_GCC:
        scriptSettings["assistanceAppFile"] = "assistanceGcc.assistanceApp"
    return [
        str(DIR_APPS_CWD).split('/')[0] + '/' + scriptSettings["assistanceAppFile"],  # @IgnorePep8
        scriptSettings["processPriority"],
        scriptSettings["dataFiles"],
        scriptSettings["TICKET"],
        scriptSettings["args"]
        ]


def getThresholds(taskDescription):  # @UnusedVariable
    '''
    Answers the question "what usage percentage of the resources is enough, and
limit, so I can perform locally? and remotely? in the case of disks, is how
many bytes are needed, and -1 or 101 to "ignore constraint"
    :param taskDescription: the task to get the thrasholds to
    '''
    # any bytes are needed, and -1 or 101 to "ignore constraint"
    thresholds = {
        "performLocal": {"memory": {}, "CPU": {}, "disk": {}},
        "performRemote": {"memory": {}, "CPU": {}, "disk": {}}}
    # memory
    # aaaalways perform local
    thresholds["performLocal"]["memory"] = {
        "physical": 101,
        "virtual": 101,
        "swap": 101}
    thresholds["performRemote"]["memory"] = {
        "physical": 101,
        "virtual": 101,
        "swap": 101}
    # CPU
    thresholds["performLocal"]["CPU"] = 101
    # adjust to decide if there will be a remote execution or not
    thresholds["performRemote"]["CPU"] = 101
    # Disk
    thresholds["performLocal"]["disk"] = -1
    thresholds["performRemote"]["disk"] = -1
    return thresholds


def getTaskPriority(taskDescription, CPUusage, memoryUsage, freeSpace):  # @UnusedVariable @IgnorePep8
    '''
    Returns the NICE value of execution of the current task,
    given the specified situation.
    Currently a STUB method that always return the same number
    :param taskDescription: the task to be priorized
    :param CPUusage: the CPU usage to priorize relative to
    :param memoryUsage: the memory usage to priorize relative to
    :param freeSpace: the disk space usage to priorize relative to
    '''
    return TUNNING_DEFAULT_PROCESS_PRIORITY


def priorityPop(ticketsList, myOfficer):
    quickestIndex = 0
    quickestApp = 10000
    orderOfComplexity = ["weka.classifiers.trees.J48",
                         "weka.classifiers.trees.DecisionStump",
                         "weka.classifiers.bayes.NaiveBayes",
                         "weka.classifiers.meta.AdaBoostM1",
                         "weka.classifiers.functions.SMO",
                         "6000",  # Parameters used for SHA256 1kb Test! @IgnorePep8
                         "6001",  # Parameters used for SHA256 8kb Test! @IgnorePep8
                         "6002",  # Parameters used for SHA256 16kb Test! @IgnorePep8
                         "2003",  # Parameters used for SHA256 128kb Test! @IgnorePep8
                         "-lcrypto",  # Parameters of the Gcc to hashblock
                         "",  # GPP/gcc for the others has no parameters!
                         "weka.classifiers.functions.MultilayerPerceptron"]
    for index, ticket in enumerate(ticketsList):
        taskApp = myOfficer.getTask(ticket).ARGUMENTS.split(" ")[0]  # @IgnorePep8
        if orderOfComplexity.index(taskApp) <= quickestApp:
            quickestApp = orderOfComplexity.index(taskApp)
            quickestIndex = index
    # print "\n\n\n\n\n\n\n\n\n"
    # print orderOfComplexity.index(taskApp)
    # print myOfficer.getTask(ticketsList[quickestIndex]).ARGUMENTS.split(" ")[0] @IgnorePep8
    # print myOfficer.getTask(ticketsList[0]).ARGUMENTS.split(" ")[0]
    popOut = ticketsList.pop(quickestIndex)
    return popOut


def schedule(myOfficer):
    while myOfficer.SCHEDULING_ACTIVE:
        schedulingMode = myOfficer.Instance.getSchedulingMode()  # @IgnorePep8
        '''
        RoundRobin simply launches every task as it comes,
        without considering local availability, order or priority
        '''
        if schedulingMode == SCHEDULE_ROUNDROBIN:
            standbyTasks = myOfficer.getStandbyTaskTickets()
            for ticket in standbyTasks:
                myOfficer.getTask(ticket).lock.set()
            myOfficer.schedulerLock.wait()
            myOfficer.schedulerLock.clear()
            '''
            First in, First out - FIFO processes tasks in the order they came,
            retaining every task until there is at least one processor free for it  # @IgnorePep8
            So, the number of active tasks is equal to the number of available processors  # @IgnorePep8
            '''
        elif schedulingMode == SCHEDULE_FIFO:
            maxRunningTasks = SCHEDULE_FIFO_MAX_PARALLEL_TASKS
            runningTasks = len(myOfficer.getPerformingTaskTickets())
            standbyTasks = myOfficer.getStandbyTaskTickets()
            while ((runningTasks < maxRunningTasks)
                   and (len(standbyTasks) > 0)
                   and myOfficer.SCHEDULING_ACTIVE):
                ticket = standbyTasks.pop(0)
                myOfficer.getTask(ticket).lock.set()
            myOfficer.schedulerLock.wait()
            myOfficer.schedulerLock.clear()
            '''
            Shortest Job First - SJF receives any number of tasks,
            executing them as they come. But, if there are more than 1 waiting,
            it will get the probable fastest one to execute, run it, and get a new  # @IgnorePep8
            so, at any given moment, there are only X tasks performing,
            X equal to the number of available processors
            '''
        elif schedulingMode == SCHEDULE_SJF:
            maxRunningTasks = SCHEDULE_SJF_MAX_PARALLEL_TASKS
            runningTasks = len(myOfficer.getPerformingTaskTickets())
            standbyTasks = myOfficer.getStandbyTaskTickets()
            while ((runningTasks < maxRunningTasks)
                   and (len(standbyTasks) > 0)
                   and myOfficer.SCHEDULING_ACTIVE):
                ticket = priorityPop(standbyTasks, myOfficer)
                myOfficer.getTask(ticket).lock.set()
            myOfficer.schedulerLock.wait()
            myOfficer.schedulerLock.clear()
