#!/usr/bin/env python
'''
Performer.py - Class of the AssistancePerformer Package with the functions to execute a task from the Assistance Officer
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time, subprocess, threading, os
# ASSISTANCE MODULE IMPORTS ----------
# ASSISTANCE OBJECT IMPORTS ------------
# ASSISTANCE CONSTANT IMPORTS -------
from cpnLibrary.implementation.Constants import *
import pkgMissionControl.implementation.Launcher
import cpnLibrary.implementation.AssistanceDBMS
        
gatherData = lambda task: pkgMissionControl.implementation.Launcher.getTransceiverInstance().gatherData(task)
getScript = lambda task: cpnLibrary.implementation.AssistanceDBMS.getCallerScript(task)
        
def callScript(taskDescription):
    #print "\nAssistance Performer started task ServiceTicket '"+str(taskDescription.TICKET)+"'\n\tCalling Script and Arguments: "+str(taskDescription.callScript)
    taskDescription.workerThreads["localPerformerScript"] = subprocess.Popen(taskDescription.SCRIPT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    taskDescription.workerThreads["localPerformerScript"].wait()
    stdout, stderr = taskDescription.workerThreads["localPerformerScript"].communicate()
    #print "\n\nAssistance Performer finished task ServiceTicket "+str(taskDescription.TICKET)+"\n\tOutput: "+str(stdout)+"\n\tErrors: "+str(stderr)
    # if the caller script was interrupted, does nothing, AND SIMPLY ENDS
    if taskDescription.TIME_INTERRUPTED == '':
        # if it finishes computing, it will acquire the lock and set the results 
        taskDescription.lock.acquire()
        taskDescription.TIME_COMPLETED = time.time()
        #setting up the results
        #If the  answer must be returned immediately, as a string that is the answer:
        if CHANNEL_IMMEDIATE == taskDescription.ANSWER_CHANNEL:
            taskDescription.STDOUT, taskDescription.STDERR = stdout, stderr
        #if the answer is the absolture path to a answer file
        elif CHANNEL_LOCAL_FILE == taskDescription.ANSWER_CHANNEL:
            filepath = lambda outType: os.path.abspath(taskDescription.OUTPUT_DIR+taskDescription.TICKET+"-"+outType+".dat")
            taskDescription.STDOUT, taskDescription.STDERR = filepath("stdout"), filepath("stderr")
        #allowing the program to continue
        taskDescription.updateStatus(STATUS_COMPLETED_LOCAL)
        taskDescription.lock.notify()
        taskDescription.lock.release()

    
    
def perform(taskDescription):
    taskDescription.updateStatus(STATUS_PERFORMING_LOCAL)
    taskDescription.DATA_LOCATION = gatherData(taskDescription) 
    taskDescription.SCRIPT = getScript(taskDescription)
    taskDescription.workerThreads["localPerformerSupporter"] = threading.Thread(target=callScript, args=(taskDescription,))
    taskDescription.workerThreads["localPerformerSupporter"].start()

    

def interrupt(taskDescription):
    if taskDescription.TIME_INTERRUPTED == '':
        taskDescription.lock.acquire()
        taskDescription.TIME_INTERRUPTED = time.time()
        taskDescription.workerThreads["localPerformerScript"].terminate()
        taskDescription.updateStatus(STATUS_INTERRUPTED_LOCAL)
        taskDescription.lock.notify()
        taskDescription.lock.release()
    
    