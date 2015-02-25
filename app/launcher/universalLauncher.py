# This Scroll runs a working version of the Assistance Function installed in the current directory
# Scroll Version: 1.0
# Linux Environment Version:    1.0
# MAC Environment Version:        0.0
# Windows Environment Version:    0.0 

import subprocess
import platform

def linuxRun():
    #print 'Running on Linux! Yaaay!'
    subprocess.call('linux/crescendo.sh')

def macRun():
    print 'Sorry, MAC OS is not supported (YET!)'

def winRun():
    print 'Sorry, Windows is not Supported. Try Ubuntu, a free Linux OS!'

def noRun():
    print 'Sorry, your current Operational System may not compatible with the Assistance Project'


currentPlatform = platform.system()
    
if currentPlatform == 'Linux':
    linuxRun()
elif currentPlatform == 'Darwin':
    macRun()
elif currentPlatform == 'Windows':
    winRun()
else:
    noRun()