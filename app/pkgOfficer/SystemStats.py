#!/usr/bin/env python
'''
Gets the data about the current situation of the host system
Jose F. R. Fonseca
See Attached License file
'''
# NATIVE MODULE IMPORTS ------------------
import os
import psutil
# ASSISTANCE CONSTANTS IMPORTS -----
from cpnLibrary.Constants import DIR_APPS_CWD


def bytes2human(n):
	'''
	Converts a integer number of bytes in a human-readable string  # @IgnorePep8
	:param n: The number of bytes to be converted  # @IgnorePep8
	SOURCE: http://code.activestate.com/recipes/578019  # @IgnorePep8
	'''  # @IgnorePep8
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')  # @IgnorePep8
	prefix = {}  # @IgnorePep8
	for i, s in enumerate(symbols):  # @IgnorePep8
		prefix[s] = 1 << (i + 1) * 10  # @IgnorePep8
	for s in reversed(symbols):  # @IgnorePep8
		if n >= prefix[s]:  # @IgnorePep8
			value = float(n) / prefix[s]  # @IgnorePep8
			return '%.1f%s' % (value, s)  # @IgnorePep8
	return "%sB" % n  # @IgnorePep8


def getMemoryUsage():
	phymem = psutil.phymem_usage()  # @IgnorePep8
	virtmem = psutil.virtmem_usage()  # @IgnorePep8
	swapmem = psutil.swap_memory()  # @IgnorePep8
	return {  # @IgnorePep8
		"physical" : phymem.percent,  # @IgnorePep8
		"virtual" : virtmem.percent,  # @IgnorePep8
		"swap" : swapmem.percent}  # @IgnorePep8


def getCPUusage():
	percentArray = psutil.cpu_percent(interval=1, percpu=True)  # @IgnorePep8
	return percentArray  # @IgnorePep8


def getFreeKbInAssistanceAppsCWD():
	path = os.path.abspath(DIR_APPS_CWD)  # @IgnorePep8
	kbytes = (psutil.disk_usage(path)[2])/1024  # @IgnorePep8
	return kbytes  # @IgnorePep8


def getFreeSpaceInAssistanceAppsCWD_HumanReadable():
	return bytes2human(psutil.disk_usage(os.path.abspath(DIR_APPS_CWD))[2])  # @IgnorePep8
