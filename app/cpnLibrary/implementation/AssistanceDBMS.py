
def getNewTicketNumber(objectHash):
    return objectHash


def getSymbol(constName, category=''):
    if category=="STATUS":
        if constName ==  'DRAFT':
            return 'DRAFT'
    
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














