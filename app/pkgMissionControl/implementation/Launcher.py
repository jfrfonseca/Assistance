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
import time


# =============================================
# ~~~~~~~~~~~~~~~~~~ Local Imports ~~~~~~~~~~~~~~~~~~
# =============================================
from pkgTransceiver.implementation.Transceiver import Transceiver

# ===================
# ------------------ Classes ------------------
# ===================

class Assistance():    
    # ===========================================
    # ~~~~~~~~~~~~~~~~~~ Constants ~~~~~~~~~~~~~~~~~~
    # ===========================================
    #general
    defaultDelay = 0.5                                      # default delay time for a socket response
    socketWarmUpTime = 2.0                           # time for a socket to be set-up
    missionControlOAuthID = "0123456789ABCDEF"         # OAuth Token ID for this package
    commonModulesLoc = "/cpnCommonLibraries/"        # Location of the folder with the common modules for all launched scripts
    
    # Transceiver
    transceiverListenningPorts = [23019, 23193, 47913]      # Ports that the Transceiver Listens to
     
     
    # ==========================================
    # ~~~~~~~~~~~~~~~~~~ Variables ~~~~~~~~~~~~~~~~~~
    # ==========================================
    # Transceiver
    transceiverOAuthToken = "0123456789ABCDEF"                      # OAuth authentication token to Mission Control talk to Transceiver
         
    # ========================================================
    # ~~~~~~~~~~~~~~~~~~ Working Directory Manipulations ~~~~~~~~~~~~~~~~~~
    # ========================================================
    
     
    # =========================================
    # ~~~~~~~~~~~~~~~~~~ Buffers ~~~~~~~~~~~~~~~~~~
    # =========================================
     
     
    # ==============================================
    # ~~~~~~~~~~~~~~~~~~ Control Objects ~~~~~~~~~~~~~~~~~~
    # ==============================================
    # general
    global droneSocket
     
    # pkgTransceiver
    global transceiver
     
    # pkgOfficer
    global officer
     
    # =====================
    # ------------------ Functions ------------------
    # =====================    
    def shutdown(self):
        self.transceiver.shutdown()
     
    # =============================================
    # ++++++++++++++++++ Constructors ++++++++++++++++++
    # =============================================
    def __init__(self):
        self.transceiver = Transceiver()
       
     
    # ============================================
    # ++++++++++++++++++ Destructors ++++++++++++++++++
    # ============================================

