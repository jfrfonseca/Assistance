#!/bin/bash
currentDirectory=$(dirname $0)
separator="--- New Assistance Time Test ----------------------"

# EXECUTION SCRIPT FOR THE MULTIPLATTFORM SETUP ON THE ASSISTANCE PROJECT
# VERSION 1.0	2015-01-26	"FIRST CLASS"
# AUTHOR: JOSÉ F.R.A. FONSECA (JFRA.FONSECA@GMAIL.COM)
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#

# initiate java class path
export CLASSPATH=$currentDirectory/weka.jar:.

# Drop new instances in each result file
echo $separator >> $currentDirectory/../tests/validation.dat
date --iso-8601=seconds >> $currentDirectory/../tests/validation.dat

echo $separator >> $currentDirectory/../tests/results.dat
date --iso-8601=seconds >> $currentDirectory/../tests/results.dat

echo $separator >> $currentDirectory/../tests/time.dat
date --iso-8601=seconds >> $currentDirectory/../tests/time.dat

# Validate test file
java -Xmx1024m weka.core.Instances $currentDirectory/../tests/weather.nominal.arff >>$currentDirectory/../tests/validation.dat

# repeat 10 times
{ time -p bash -c "
for i in {1..10}
do
	# Classify test file
	java -Xmx1024m weka.classifiers.trees.J48 -t $currentDirectory/../tests/weather.nominal.arff -i >>$currentDirectory/../tests/results.dat
done
" ; } 2>>$currentDirectory/../tests/time.dat
