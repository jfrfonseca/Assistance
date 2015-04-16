
from cpnLibrary.implementation.Constants import *


def getCallerScript(taskDescription):
    #ALL ARGUMENTS COME AS A STRING - the data they refer may differ. EVERY ASSISTANCEAPP MUST HAVE A DEFAULT DATA FILES (DATA AND ANSWER) FOLDER, AND THIS FOLDER WILL DE SUBSCRIBED IN THE DBMS FOR EACH APP, SO THE APP CAN CALL ITS FILES FROM THE DEFAULT
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
        
    return [DIR_APPS_CWD+scriptSettings["assistanceAppFile"], scriptSettings["processPriority"], scriptSettings["dataFiles"], scriptSettings["TICKET"], scriptSettings["args"]]




def getThresholds(taskDescription):
    #ansers the question "what usage percentage of the resources is enough, and limit, so I can perform locally? and remotelly? in the case of disks, is how many bytes are needed, and -1 or 101 to "ignore constraint"
    thresholds = {"performLocal":{"memory":{}, "CPU":{}, "disk":{}}, "performRemote":{"memory":{}, "CPU":{}, "disk":{}}}
    #memory
    #aaaalways perform local
    thresholds["performLocal"]["memory"]["minimum"] = {"physical" : -1, "virtual" : -1, "swap" : -1}
    thresholds["performLocal"]["memory"]["maximum"] = {"physical" : 101, "virtual" : 101, "swap" : 101}    
    thresholds["performRemote"]["memory"]["priorityIncreaseDelta"] = 10  
    #adjust to decide if there will be a remote execution or not
    thresholds["performRemote"]["memory"]["minimum"] = {"physical" : -1, "virtual" : -1, "swap" : -1}
    thresholds["performRemote"]["memory"]["maximum"] = {"physical" : 101, "virtual" : 101, "swap" : 101}
    thresholds["performRemote"]["memory"]["priorityIncreaseDelta"] = 10 
    #CPU
    #always perform local
    thresholds["performLocal"]["CPU"]["minimum"] = -1
    thresholds["performLocal"]["CPU"]["maximum"] = 101
    thresholds["performRemote"]["CPU"]["priorityIncreaseDelta"] = 10  
    #adjust to decide if there will be a remote execution or not
    thresholds["performRemote"]["CPU"]["minimum"] = -1
    thresholds["performRemote"]["CPU"]["maximum"] = 101
    thresholds["performRemote"]["CPU"]["priorityIncreaseDelta"] = 10  
    #Disk
    #OK, the maximum is not a percentage. Only AFTER I get a computer that has MORE than a PetaByte FREE in space, you can tell me "I told you so", figure-of-speech me from the future! Remember, smartass, those amounts are in KBs!
    thresholds["performLocal"]["disk"]["minimum"] = -1
    thresholds["performLocal"]["disk"]["maximum"] = 1000000000000000    
    thresholds["performRemote"]["disk"]["minimum"] = -1
    thresholds["performRemote"]["disk"]["maximum"] = 1000000000000000
    
    return thresholds


def getTaskPriority(taskDescription, CPUusage, memoryUsage, freeSpace):
    #temporarily a #STUB that does not modify the task's priority
    return TUNNING_DEFAULT_PROCESS_PRIORITY






