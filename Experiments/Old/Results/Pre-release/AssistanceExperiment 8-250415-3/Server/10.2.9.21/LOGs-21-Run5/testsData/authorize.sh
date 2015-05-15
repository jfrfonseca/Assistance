#!/bin/bash
# CHMOD's Assistance in order to allow it to run
# CWD is build/testsData
# Macros
AUTH_LEVEL=755
APPS_DIR=../AssistanceApps
# Authorizes
chmod ${AUTH_LEVEL} cleanUp.sh
chmod ${AUTH_LEVEL} ../testAssistance
chmod ${AUTH_LEVEL} ${APPS_DIR}/assistanceWEKA.assistanceApp
chmod ${AUTH_LEVEL} ${APPS_DIR}/echoInAllCaps.assistanceApp
chmod ${AUTH_LEVEL} ${APPS_DIR}/sha256Example.assistanceApp
chmod ${AUTH_LEVEL} ${APPS_DIR}/sha256/V0.5/linux/bin/main.build
