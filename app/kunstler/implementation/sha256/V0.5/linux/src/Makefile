# MAKEFILE FOR THE SHA256-V0.5 FUNCTION OF THE ASSISTANCE PROJECT
# VERSION 0.3	2015-01-18	"INITIAL SETUP"
# AUTHOR: JOSÉ F.R.A. FONSECA (JFRA.FONSECA@GMAIL.COM)
# LICENSE: MIT (http://opensource.org/licenses/MIT)
#
CC 		= g++
CFLAGS		= -O
BINLOC		= ../bin/
SRCLOC		= 
TSTLOC2BIN		= ../../tests/
FUNCNAME	= Assistance.sha256

all: clean main

main:  mainTest.cpp 
	${CC} ${CFLAGS} ${SRCLOC}mainTest.cpp ${SRCLOC}sha256.cpp -o ${BINLOC}main.build 

test0:  
	time -p ./${BINLOC}main.build ${TSTLOC2BIN}test0data.dat 100 ve

test1:  
	time -p ./${BINLOC}main.build ${TSTLOC2BIN}test0data.dat 1000000 ve

test2:  
	time -p ./${BINLOC}main.build ${TSTLOC2BIN}test0data.dat 10000000

testAll: test0 test1 test2

testExperiment:
	time -p ./${BINLOC}main.build ${TSTLOC2BIN}experimentData.dat 50000

clean:
	 rm -f ${BINLOC}*.o ${BINLOC}*.build 

