#!/usr/bin/env python
'''
Performer.py - Class of the AssistancePerformer Package with the functions to execute a task from the Assistance Officer
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time, subprocess, os
# ASSISTANCE MODULE IMPORTS ----------
# ASSISTANCE OBJECT IMPORTS ------------
# ASSISTANCE CONSTANT IMPORTS -------
from cpnLibrary.implementation.Constants import *

    
def perform(task):
    task.updateStatus(STATUS_PERFORMING_LOCAL)
    task.workerThreads["localPerformerScript"] = subprocess.Popen(task.SCRIPT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    task.workerThreads["localPerformerScript"].wait()
    stdout, stderr = task.workerThreads["localPerformerScript"].communicate()
    # if the caller script was interrupted, does nothing, AND SIMPLY ENDS
    if task.TIME_INTERRUPTED == NULL:
        # if it finishes computing, it will acquire the lock and set the results, then unlock, to avoid double finishing
        task.TIME_COMPLETED = time.time()
        if CHANNEL_IMMEDIATE == task.ANSWER_CHANNEL:
            task.STDOUT, task.STDERR = stdout, stderr
        else:
            filepath = lambda outType: os.path.relpath(task.OUTPUT_DIR+task.TICKET+"-"+outType+".dat")
            task.STDOUT, task.STDERR = filepath("stdout"), filepath("stderr")
        task.updateStatus(STATUS_COMPLETED_LOCAL)
        task.lock.set()
    

def interrupt(taskDescription):
    if taskDescription.TIME_INTERRUPTED == NULL:
        taskDescription.TIME_INTERRUPTED = time.time()
        taskDescription.workerThreads["localPerformerScript"].terminate()
        taskDescription.updateStatus(STATUS_INTERRUPTED_LOCAL)
        taskDescription.lock.set()
    
    