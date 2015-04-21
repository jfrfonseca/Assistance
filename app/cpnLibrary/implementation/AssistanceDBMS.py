#!/usr/bin/env python
'''
AssistanceDBMS.py - Returns data to the Assisance System runtime
from the data warehouse facility
Jose F. R. Fonseca
See Attached License file
'''
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.implementation.Constants import\
    AppID_LOCAL_ECHO_TEST, AppID_SHA256_TEST, AppID_SHA256_REMOTE_TEST,\
    NULL, DIR_APPS_CWD, TUNNING_DEFAULT_PROCESS_PRIORITY, AppID_WEKA


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
    scriptSettings["dataFiles"] = str(taskDescription.DATA_LOCATION)
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
    return [
        DIR_APPS_CWD + scriptSettings["assistanceAppFile"],
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
