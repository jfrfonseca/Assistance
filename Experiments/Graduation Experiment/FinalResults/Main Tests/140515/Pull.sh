#!/bin/bash
for server in `cat allServersList`; do
	scp 405808@$server:/home/405808/build-Server/*.zip $(dirname $0)/Results
done
