#!/bin/bash
for server in `cat allServersList`; do
	scp -r ../build-Server 405808@$server:/home/405808/
done
for server in `cat allServersList`; do
	ssh $server < authorizer.sh.script
done
