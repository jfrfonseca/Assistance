#!/bin/bash
chmod 755 authorize.sh
./authorize.sh
./cleanUp.sh
cd ../
./testAssistance -f
mv LOGs.zip LOGs-Baseline.zip
sleep 100
./testAssistance -s
