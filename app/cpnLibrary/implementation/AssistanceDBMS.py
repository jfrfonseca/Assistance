

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
        return ["AssistanceApps/echoInAllCaps.assistanceApp", args, assistanceAppDataFolder]
    elif taskDescription.appID == "ASSISTANCE_SHA256_TEST":
        return ["AssistanceApps/sha256Example.assistanceApp", args, assistanceAppDataFolder]


def getThresholds(taskDescription, request=False):
    #memory
    thresholds = {"physical" : 0, "virtual" : 0, "swap" : 0}
    #CPU
    thresholds["CPU"]=0
    return thresholds











