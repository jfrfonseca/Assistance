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
from pkgOfficer.implementation.Officer import Officer

# ====================
# ------------------ Objects ------------------
# ==================== 
global transceiver
global officer


# =====================
# ------------------ Functions ------------------
# =====================    
def shutdown():
    global transceiver
    transceiver.shutdown()
        

def setup():
    global transceiver
    global officer
    transceiver = Transceiver()
    officer = Officer()
    
def getOfficerInstance():
    global officer
    return officer
       
     
    # ============================================
    # ++++++++++++++++++ Destructors ++++++++++++++++++
    # ============================================

