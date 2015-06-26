#!/bin/bash
currentDirectory=$(dirname $0)

# EXECUTION SCRIPT FOR THE LINUX SETUP OF THE ASSISTANCE PROJECT
# VERSION 0.5	2015-01-18	"1SEC EXPERIMENT"
# AUTHOR: JOSÉ F.R.A. FONSECA (JFRA.FONSECA@GMAIL.COM)
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

time -p ./$currentDirectory/bin/main.build $currentDirectory/../tests/randomFile16kb 6000 -verbose 2000
