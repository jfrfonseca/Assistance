import psutil, os

def bytes2human(n):
	# http://code.activestate.com/recipes/578019
	# >>> bytes2human(10000)
	# '9.8K'
	# >>> bytes2human(100001221)
	# '95.4M'
	symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i + 1) * 10
	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '%.1f%s' % (value, s)
	return "%sB" % n
	
def getMemoryUsage():
	phymem = psutil.phymem_usage()
	virtmem = psutil.virtmem_usage()
	swapmem = psutil.swap_memory()
	return {"physical" : phymem.percent, "virtual" : virtmem.percent, "swap" : swapmem.percent}


def getCPUusage():
	percentArray = psutil.cpu_percent(interval=1, percpu=True)
	return percentArray

def getFreeSpaceInDiskPartition(mountpoint):
	return bytes2human(psutil.disk_usage(mountpoint).free)

def getDiskFreeSpace():
	spaceArray = []
	for part in psutil.disk_partitions(all=False):
		if os.name == 'nt':
			if 'cdrom' in part.opts or part.fstype == '':
				# skip cd-rom drives with no disk in it; they may raise ENOENT, pop-up a Windows GUI error for a non-ready partition or just hang.
				continue
		spaceArray.append(getFreeSpaceInDiskPartition(part.mountpoint))			
	return spaceArray

