# ==============================================
# ~~~~~~~~~~~~~~~~~~ System Imports ~~~~~~~~~~~~~~~~~~
# ==============================================
import os, sys


# =============================================
# ~~~~~~~~~~~~~~~~~~ Local Imports ~~~~~~~~~~~~~~~~~~
# =============================================


# ==============================================
# ~~~~~~~~~~~~~~~~~~ Remote Imports ~~~~~~~~~~~~~~~~~~
# ==============================================
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
import ami  # @UnresolvedImport

cpuUsage = ami.getCPUusage()
memUsage = ami.getMemoryUsage()
freeDisk = ami.getDiskFreeSpace()
print "CPU Usage, per CPU: "
print cpuUsage
print "Memory Usage (physical, virtual, swap): "
print memUsage
print "Free space per partition in disk: "
print freeDisk