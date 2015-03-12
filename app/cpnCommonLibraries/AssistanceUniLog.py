from time import time



class LogOutput():
    
    DEFAULT_LOGOUTPUT_NAME = "UniLog Output 0"
    CURRENT_NAME = 1
    TIME_INIT = 0
    UNILOG_LOGGER_NAME = 'UniLogger0'
    CURRENT_PRIORITY = 2
    
    def __init__(self, newLogOutName=DEFAULT_LOGOUTPUT_NAME, loggerName=UNILOG_LOGGER_NAME):
        self.CURRENT_NAME = newLogOutName
        self.LOGGER_NAME = loggerName
        self.TIME_INIT = time.time()
        print "#UniLog Output '"+self.CURRENT_NAME+"' :: "+str(self.TIME_INIT)
        
    def output(self, loggerName, message, priority=CURRENT_PRIORITY):
        newLineString = "|"
        if(priority > self.CURRENT_PRIORITY):
            self.CURRENT_PRIORITY = priority
            newLineString += "\\\n"
        elif(priority < self.CURRENT_PRIORITY):
            self.CURRENT_PRIORITY = priority
            newLineString += "/\n"
        for curCol in range(self.CURRENT_PRIORITY):
            newLineString += "|"
            
        newLineString += "- @"+str(loggerName)+": '"+str(message)+"' -+- "+str(time.time()-self.TIME_INIT)
            
        print newLineString
        

class AssistanceUniLog():
    
    DEFAULT_VERBOSITY = 1
    CURRENT_VERBOSITY = 1
    COUNTER_MESSAGE = 0
    DEFAULT_LOGGER_NAME = "Assistance Unified Logger"
    DEFAULT_PRIORITY = -1
    
    logOutput = -1
    
    
    def counterMessage(self, loggerName=DEFAULT_LOGGER_NAME):
        self.logOutput.output(loggerName+':'+str(self.COUNTER_MESSAGE))
        self.COUNTER_MESSAGE += 1
        
    
    def __init__(self, newLogOutput=-1, newDefaultVerbosity=1):
        self.DEFAULT_VERBOSITY = newDefaultVerbosity
        self.logOutput = newLogOutput
        if (self.logOutput == -1): self.logOutput = LogOutput()
    
    def uniLog(self, loggerName=DEFAULT_LOGGER_NAME, requiredVerbosity=DEFAULT_VERBOSITY, message=counterMessage(), priority = DEFAULT_PRIORITY):
        if (self.CURRENT_VERBOSITY > requiredVerbosity):
            self.logOutput.output(loggerName, message, priority)

        