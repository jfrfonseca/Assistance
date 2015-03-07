# 
# __ASSISTANCE MISSION CONTROL LAUNCHER__ 0.5.030315
# 
# Copyright (c) 2015, Jose F. Fonseca <jose.f.fonseca@ieee.org>
# 
# SEE THE ATTACHED LICENSE FILE FOR IMPORTANT LEGAL INFORMATIONS
#  
# Launches 
# - This version requires a web browser, mostly because nodeJS does not support WebRTC - yet.
# - This version requires Google Chrome as the web browser, due its dependence on webkit. working on it.


# ==============================================
# ~~~~~~~~~~~~~~~~~~ System Imports ~~~~~~~~~~~~~~~~~~
# ==============================================
import subprocess, time, socket


# =============================================
# ~~~~~~~~~~~~~~~~~~ Local Imports ~~~~~~~~~~~~~~~~~~
# =============================================


# ===========================================
# ~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~
# ===========================================
#general
defaultDelay = 0.5                                      # default delay time for a socket response
socketWarmUpTime = 2.0                           # time for a socket to be set-up
missionControlOAuthID = "MiCtrl"

# Transceiver
assistanceRootFolderLoc = "../../../"              # Root folder of the Assistance System
transceiverScriptLoc = assistanceRootFolderLoc+"transceiver/implementation/tests/all/echoServer.py"       # Assistance Transceiver Launcher Script
transceiverScriptArgs = ["python", transceiverScriptLoc]             # command to launch the Assistance Transceiver Launcher Script
transceiverListenningPorts = [23019, 23193, 47913]                  # Ports that the Transceiver Listens to



# ==========================================
# ~~~~~~~~~~~~~~~~~~ Variables ~~~~~~~~~~~~~~~~~~
# ==========================================
# Transceiver
transceiverOAuthToken = "0000000000000000"                      # OAuth authentication token to Mission Control talk to Transceiver
transceiverEchoTestString = "MissionControl_>_Transceiver\t"+str(int(time.time()))+"\tAckSetup\t"+missionControlOAuthID+":"+transceiverOAuthToken    # String passed to the Transceiver Port to test it
# =========================================
# ~~~~~~~~~~~~~~~~~~ Buffers ~~~~~~~~~~~~~~~~~~
# =========================================


# ==============================================
# ~~~~~~~~~~~~~~~~~~ Control Objects ~~~~~~~~~~~~~~~~~~
# ==============================================
# general
global droneSocket

# transceiver
global transceiverObject


# ===================
# ------------------ Classes ------------------
# ===================
def socketThread(port):
    droneSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverObject.serveforever()

# =====================
# ------------------ Functions ------------------
# =====================
def testTransceiverSetup(portNumbers):
    host = 'localhost'
    size = 10000
    for port in portNumbers:
        print "Testing the connection to Transceiver on port "+str(port)
        time.sleep(defaultDelay)
        droneSocket.connect((host,port))
        time.sleep(defaultDelay)
        droneSocket.send(transceiverEchoTestString)
        time.sleep(defaultDelay)
        answer = droneSocket.recv(size)
        if answer != transceiverEchoTestString:
            print "exception"
            raise Exception("Transceiver Setup Error! Port: "+str(port)+";\n\tMessage Expected: "+transceiverEchoTestString+";\n\tMessage Received: "+answer)
        print "Transceiver on port "+str(port)+" echoed: "+answer
    print "Transceiver Setup Complete"


# =========================================
# ++++++++++++++++++ Setup ++++++++++++++++++
# =========================================
# Initiate the drone control socket
print "initiating the drone control socket"
droneSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
time.sleep(socketWarmUpTime)
# initiate the transceiver service
transceiverObject  = subprocess.Popen(transceiverScriptArgs)
print "initiating the Transceiver Process"
time.sleep(socketWarmUpTime)
testTransceiverSetup(transceiverListenningPorts)
# ============================================
# ++++++++++++++++++ Teardown ++++++++++++++++++
# ============================================
droneSocket.close()
transceiverObject.kill()
 
 
 
 

