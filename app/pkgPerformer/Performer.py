#!/usr/bin/env python
'''
Performer.py - Class of the AssistancePerformer Package with the functions to
execute a task from the Assistance Officer
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import time
import subprocess
import os
# ASSISTANCE CONSTANT IMPORTS -------
from cpnLibrary.Constants import\
    STATUS_PERFORMING_LOCAL, STATUS_INTERRUPTED_LOCAL, STATUS_COMPLETED_LOCAL,\
    CHANNEL_IMMEDIATE, NULL, DIR_APPS_CWD


def perform(task):
    '''
    Sets the task's status to performing, creates a thread that calls
the script, and waits until it is finished.
The Script calling thread may be interrupted externally
If this execution finished normally, the STDOUT and STDERR of the script
    are sent to the task, and stored. THen the status of the task is set to
    completed
    :param task: the task to perform
    '''
    task.updateStatus(STATUS_PERFORMING_LOCAL)
    task.workerThreads["localPerformerScript"] = subprocess.Popen(
        task.SCRIPT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True)
    task.workerThreads["localPerformerScript"].wait()
    stdout, stderr = task.workerThreads["localPerformerScript"].communicate()
    # if the caller script was interrupted, does nothing, AND SIMPLY ENDS
    if task.TIME_INTERRUPTED == NULL:
        # if it finishes computing, it will acquire the lock and set the results, @IgnorePep8
        # then unlock, to avoid double finishing
        task.TIME_COMPLETED = time.time()
        if CHANNEL_IMMEDIATE == task.ANSWER_CHANNEL:
            task.STDOUT, task.STDERR = stdout, stderr
        else:
            filepath = lambda outType: os.path.relpath(
                DIR_APPS_CWD+task.TICKET+"/"+task.TICKET+"-"+outType+".dat")
            task.STDOUT, task.STDERR = filepath("stdout"), filepath("stderr")
        task.updateStatus(STATUS_COMPLETED_LOCAL)
        task.lock.set()


def interrupt(taskDescription):
    '''
Cleanly interrupts the thread, sets the status, and releases the director thread  # @IgnorePep8
    :param taskDescription:the running task to interrupt
    '''
    if taskDescription.TIME_INTERRUPTED == NULL:
        taskDescription.TIME_INTERRUPTED = time.time()
        taskDescription.workerThreads["localPerformerScript"].terminate()
        taskDescription.updateStatus(STATUS_INTERRUPTED_LOCAL)
        taskDescription.lock.set()
