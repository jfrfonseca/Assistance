# CONSTANTS
#TESTS VERSION
    #TOKENS
TOKEN_TRANSCEIVER_TEST = "0123456789ABCDEF"
    #TEST AssistanceApps
AppID_LOCAL_ECHO_TEST = "LOCAL_ECHO_TEST"
AppID_SHA256_TEST = "SHA256_TEST"

#DEFAULT VALUES
#SYMBOLS
NOT_APPLYED = "NOT_APPLYED"
#TIMES
TIME_SOCK_COOLDOWN = 0.0
#PORTS
PORT_API_REQUESTS = 29112
#TYPES
TYPE_API_REQUEST_MSG = "MSG_API_REQUEST"
TYPE_API_REQUEST_ANS = "ANS_API_REQUEST"
#CHANNELS
CHANNEL_LOCAL_FILE = "LOCAL_FILE"
#TASK STATUS
STATUS_DRAFT = "DRAFT"
STATUS_WAITING = "WAITING"
STATUS_PERFORMING_LOCAL = "PERFORMING_LOCAL"
STATUS_COMPLETED_LOCAL = "COMPLETED_LOCAL"
STATUS_INTERRUPTED_LOCAL = "INTERRUPTED_LOCAL"






def getCallerScript(taskDescription):
    #ALL ARGUMENTS COME AS A STRING - the data they refer may differ. EVERY ASSISTANCEAPP MUST HAVE A DEFAULT DATA FILES (DATA AND ANSWER) FOLDER, AND THIS FOLDER WILL DE SUBSCRIBED IN THE DBMS FOR EACH APP, SO THE APP CAN CALL ITS FILES FROM THE DEFAULT
    args = taskDescription.appArgs
    if args == NOT_APPLYED:
        args = ""
        
    if taskDescription.appID == AppID_LOCAL_ECHO_TEST:
        return ["AssistanceApps/echoInAllCaps.assistanceApp", str(taskDescription.localProcessPriority), args, str(taskDescription.gatheredDataLocation)]
    elif taskDescription.appID == AppID_SHA256_TEST:
        return ["AssistanceApps/sha256Example.assistanceApp", str(taskDescription.localProcessPriority), args, str(taskDescription.gatheredDataLocation)]





def getThresholds(taskDescription, request=False):
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
    thresholds["performLocal"]["disk"]["minimum"] = -1
    thresholds["performLocal"]["disk"]["maximum"] = -1     
    thresholds["performRemote"]["disk"]["minimum"] = -1
    thresholds["performRemote"]["disk"]["maximum"] = -1
    
    return thresholds








