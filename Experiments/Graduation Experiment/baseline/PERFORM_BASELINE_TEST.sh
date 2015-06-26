#!/bin/bash
echo "BASELINE TEST FOR $1 - ALL WEKA FUNCTIONS, SEQUENTIAL AND TIMED"
echo "Setting up"
chmod 755 baselinePerformanceWEKA.sh
chmod 755 parseResults.py
echo "Performing tests"
./baselinePerformanceWEKA.sh &> times.txt
echo "Parsing results"
(python parseResults.py) >> parsedResults.txt