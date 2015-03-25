
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
    if taskDescription.appID == "ASSISTANCE_ECHO_TEST":
        return ["AssistanceApps/echoInAllCaps.assistanceApp", taskDescription.args]
    elif taskDescription.appID == "ASSISTANCE_SHA256_TEST":
        return ["AssistanceApps/sha256Example.assistanceApp"]















