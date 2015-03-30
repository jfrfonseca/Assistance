
def validMessageKind(msgKind):
    return ( (msgKind == getSymbol("NEW_REQUEST", "MESSAGE_KIND")) or  (msgKind == getSymbol("STATUS_CHECK", "MESSAGE_KIND")) )


def getNewTicketNumber(objectHash):
    return objectHash


def getSymbol(constName, category=''):
    if category=="STATUS":
        if constName ==  'DRAFT':
            return 'DRAFT'
        if constName == 'WAITING':
            return 'WAITING'
        if constName == 'PERFORMING-LOCAL':
            return 'PERFORMING-LOCAL'
        if constName == 'PERFORMING-PEER':
            return 'PERFORMING-PEER'
        if constName == 'COMPLETED-LOCAL':
            return 'COMPLETED-LOCAL'
        if constName == 'COMPLETED-PEER':
            return 'COMPLETED-PEER'
        if constName == 'INTERRUPTED-LOCAL':
            return 'INTERRUPTED-LOCAL'
        if constName == 'INTERRUPTED-PEER':
            return 'INTERRUPTED-PEER'
    
    elif category=="CHANNEL":
        if constName ==  'IMMEDIATE':
            return 'IMMEDIATE'
        
    elif category=="MESSAGE_KIND":
        if constName ==  'NEW_REQUEST':
            return 'NEW_REQUEST'
        if constName ==  'STATUS_CHECK':
            return 'STATUS_CHECK'
        
    else:
        if constName == 'NONE':
            return 'NONE'
        if constName == 'LOCALHOST':
            return 'LOCALHOST'
        else:
            return 0
        
        
def getPort(constName):
    if constName ==  'API_REQUEST':
        return 29112
    else:
        return 0
    
    
def getToken(tokenHolder):
    if tokenHolder ==  'API_REQUEST':
        return '0123456789ABCDEF'
    else:
        return ''
    
    
def getCallerScript(taskDescription):
    #ALL ARGUMENTS COME AS A STRING - the data they refer may differ. EVERY ASSISTANCEAPP MUST HAVE A DEFAULT DATA FILES (DATA AND ANSWER) FOLDER, AND THIS FOLDER WILL DE SUBSCRIBED IN THE DBMS FOR EACH APP, SO THE APP CAN CALL ITS FILES FROM THE DEFAULT
    args = ""
    if(taskDescription.appArgs == getSymbol("NONE")):
        args = ""
    else:
        args = taskDescription.appArgs
        
    #Stub METHOD
    assistanceAppDataFolder = ""
    if taskDescription.appID == "ASSISTANCE_ECHO_TEST":
        return ["AssistanceApps/echoInAllCaps.assistanceApp", str(taskDescription.localProcessPriority), args, assistanceAppDataFolder]
    elif taskDescription.appID == "ASSISTANCE_SHA256_TEST":
        return ["AssistanceApps/sha256Example.assistanceApp", str(taskDescription.localProcessPriority), args, assistanceAppDataFolder]


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








