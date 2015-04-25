#!/bin/bash
# runs a few times the current test
# 10 runs
cd build
echo "run1"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run2"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run3"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run4"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run5"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run6"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run7"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14
 sleep 100
echo "run8"
./testAssistance -f -a 10.2.9.11 -a 10.2.9.12 -a 10.2.9.13 -a 10.2.9.14

