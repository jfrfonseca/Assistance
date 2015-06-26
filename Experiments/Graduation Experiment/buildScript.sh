#!/bin/bash
cxfreeze ../../app/startAssistance.py --target-dir build-Server
cxfreeze ../../app/ClientScript_Pyhton.py --target-dir build-Client
cxfreeze ../../app/ClientScript_NSB.py --target-dir build-NSBClient

