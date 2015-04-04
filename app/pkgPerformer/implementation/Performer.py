import time, subprocess, threading
from cpnLibrary.implementation import AssistanceDBMS
import pkgMissionControl.implementation.Launcher
from cpnLibrary.implementation.AssistanceDBMS import STATUS_COMPLETED_LOCAL,\
    STATUS_PERFORMING_LOCAL, STATUS_INTERRUPTED_LOCAL
        
        
def callScript(taskDescription):
    print "\nAssistance Performer started task ServiceTicket '"+str(taskDescription.ticket)+"'\n\tCalling Script and Arguments: "+str(taskDescription.callScript)
    taskDescription.workerThreads["localPerformerScript"] = subprocess.Popen(taskDescription.callScript, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    taskDescription.workerThreads["localPerformerScript"].wait()
    output, errors = taskDescription.workerThreads["localPerformerScript"].communicate()
    print "\n\nAssistance Performer finished task ServiceTicket "+str(taskDescription.ticket)+"\n\tOutput: "+str(output)+"\n\tErrors: "+str(errors)
    # if the caller script was interrupted, does nothing, AND SIMPLY ENDS
    if taskDescription.timeInterrupted == '':
        # if it finishes computing, it will acquire the lock and set the results 
        taskDescription.lock.acquire()
        taskDescription.timeCompleted = time.time()
        taskDescription.answer["output"]=output
        taskDescription.answer["errors"]=errors
        taskDescription.updateStatus(STATUS_COMPLETED_LOCAL)
        taskDescription.lock.notify()
        taskDescription.lock.release()

    
    
def perform(taskDescription):
    taskDescription.updateStatus(STATUS_PERFORMING_LOCAL)
    taskDescription.gatheredDataLocation = pkgMissionControl.implementation.Launcher.getTransceiverInstance().gatherData(taskDescription) 
    taskDescription.callScript = AssistanceDBMS.getCallerScript(taskDescription)
    taskDescription.workerThreads["localPerformerSupporter"] = threading.Thread(target=callScript, args=(taskDescription,))
    taskDescription.workerThreads["localPerformerSupporter"].start()

    

def interrupt(taskDescription):
    taskDescription.timeInterrupted = time.time()
    taskDescription.workerThreads["localPerformerScript"].terminate()
    taskDescription.updateStatus(STATUS_INTERRUPTED_LOCAL)
    
    