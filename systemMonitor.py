import string
import os
import commands
import time
import psutil

''' All system monitors will use this interface '''
class systemMonitor():
	filedValues = {}

	def __init__(self):
		self.fieldValues = {}

	def getFieldValue(self, name):
		result = self.fieldValues[name]
		if not result or result == '':
			result = 'no data'
		return result;

	def update(self):
		raise NotImplementedError( 'systemMonitor: update not implemented')


class systemMonitorMemInfo(systemMonitor):

	def __init__(self):
		systemMonitor.__init__(self)

	#Updates the information we have from the meminfo file
	#Each row of the file is in the following format 
	#Name:        Int kB
	def update(self):
		meminfo = open('/proc/meminfo', 'r')
		if meminfo:
			for line in meminfo:
				words = string.split(line)
				if len(words) > 2:
					name = words[0][:-1]
					self.fieldValues[name] = words[1] + words[2]


#TODO:
class systemMonitorInterrupts(systemMonitor):

	def __init__(self):
		systemMonitor.__init__(self)

	#          CPU0       CPU1       CPU2       CPU3       
	#0:         28          0          0          0   IO-APIC-edge      timer
	def update(self):
		interruptFile = open('/proc/interrupts', 'r')
		if interruptFile:
			#get number of CPUs from the first line
			firstLine = interruptFile.readline()
			cpuCount = len(string.split(firstLine))
			for line in interruptFile:
				words = string.split(line)
				interruptID = words[0][:-1] #trim off the colon
				cpuValues = []
				for i in range(cpuCount):
					print i





''' For this CPU stats we will convert user_hz to seconds 
	The file format is the following
	CPU usr nice sys iowait irq soft steal guest gnice idle
	...
No:	intr # # # # ... (x713 where the first is the total)
	ctxt #
	btime #
	processes #
	procs_running #
	procs_blocked #
	softirq # # # # # # # # # # #
'''
class systemMonitorCPUUtilization(systemMonitor):
	#the /proc/stat file is in terms of user hz, which is most often 100
	user_hz = 100

	def __init__(self):
		systemMonitor.__init__(self)
		#this grabs the current architechture's user_hz
		user_hz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])


	def update(self):
		dataFile = open('/proc/stat', 'r')
		if dataFile:
			for line in dataFile:
				if line.startswith('cpu'):
					localFields = string.split(line)
					name = localFields[0]
					self.fieldValues[name + '_usr'] = int(localFields[1]) / self.user_hz
					self.fieldValues[name + '_nice'] = int(localFields[2]) / self.user_hz
					self.fieldValues[name + '_sys'] = int(localFields[3]) / self.user_hz
					self.fieldValues[name + '_iowait'] = int(localFields[4]) / self.user_hz
					self.fieldValues[name + '_irq'] = int(localFields[5]) / self.user_hz
					self.fieldValues[name + '_soft'] = int(localFields[6]) / self.user_hz
					self.fieldValues[name + '_steal'] = int(localFields[7]) / self.user_hz
					self.fieldValues[name + '_guest'] = int(localFields[8]) / self.user_hz
					self.fieldValues[name + '_gnice'] = int(localFields[9]) / self.user_hz
					self.fieldValues[name + '_idle'] = int(localFields[10]) / self.user_hz
				elif line.startswith('intr'):
					print 'Interrupt mapping not implemented for proc/stat'
				elif line[:3] == 'softirq':
					print 'Soft Interrupts mapping not implemented for proc/stat'
				elif line.startswith('btime'):
					localFields = string.split(line)
					name = localFields[0]
					self.fieldValues[name] = time.gmtime(float(localFields[1]))
				else:
					#The rest of the fields are straight numbers and don't need special treatment
					localFields = string.split(line)
					name = localFields[0]
					self.fieldValues[name] = localFields[1]


class systemMonitorCPUSaturation(systemMonitor):

	def __init__(self):
		systemMonitor.__init__(self)


	def update(self):
		cpu_count = commands.getoutput('cat /proc/cpuinfo | grep processor | wc -l')
		data = commands.getoutput('vmstat')
		lines = string.split(data, '\n')
		procs_waiting = string.split(lines[-1])[0]
		
		self.fieldValues['cpu_count'] = cpu_count
		self.fieldValues['cpu_saturation'] = float(procs_waiting)/float(cpu_count)


class systemMonitorMemoryCapacityUtilization(systemMonitor):
	def __init__(self):
		systemMonitor.__init__(self)

	#Updates the information we have from the meminfo file
	#Each row of the file is in the following format 
	#Name:        Int kB
	def update(self):
		meminfo = open('/proc/meminfo', 'r')
		if meminfo:
			for line in meminfo:
				words = string.split(line)
				if len(words) > 2:
					name = words[0][:-1]
					self.fieldValues[name] = words[1] + words[2]


class systemMonitorMemoryCapacitySaturization(systemMonitor):
	def __init__(self):
		systemMonitor.__init__(self)

	#Here we use the measure of data swapped in from disk and swapped to disk to measure saturation
	#once we hit capacity we have to swap out memory to disk to make room for more data
	#a good measure of saturation then is the ratio of amount swapped in to the amount swapped out
	def update(self):
		data = commands.getoutput('vmstat')
		lines = string.split(data, '\n')
		data_line = string.split(lines[-1])

		#data should be in the following format:
		#procs -----------memory---------- ---swap-- -----io---- -system-- ----cpu----
		# r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa

		self.fieldValues['swapped_in'] = int(data_line[6])
		self.fieldValues['swapped_out'] = int(data_line[7])
		#check for zero denominator
		saturation = 0
		if (int(data_line[7]) > 0):
			saturation = swapped_in / swapped_out
		self.fieldValues['saturation'] = saturation

class systemMonitorStorageDeviceIOUtilization(systemMonitor):
	def __init__(self):
		systemMonitor.__init__(self)

	def update(self):
		systemStats = psutil.disk_io_counters(perdisk=False)

		name = 'Total'
		self.fieldValues[name + '_read_count']	= systemStats.read_count
		self.fieldValues[name + '_write_count']	= systemStats.write_count
		self.fieldValues[name + '_read_bytes']	= systemStats.read_bytes
		self.fieldValues[name + '_write_bytes']	= systemStats.write_bytes
		self.fieldValues[name + '_read_time']	= systemStats.read_time
		self.fieldValues[name + '_write_time']	= systemStats.write_time



		for name, stats in psutil.disk_io_counters(perdisk=True).iteritems():
			self.fieldValues[name + '_read_count']	= stats.read_count
			self.fieldValues[name + '_write_count']	= stats.write_count
			self.fieldValues[name + '_read_bytes']	= stats.read_bytes
			self.fieldValues[name + '_write_bytes']	= stats.write_bytes
			self.fieldValues[name + '_read_time']	= stats.read_time
			self.fieldValues[name + '_write_time']	= stats.write_time


class systemMonitorStorageDeviceIOSaturation(systemMonitor):
	def __init__(self):
		systemMonitor.__init__(self)

	def update(self):
		data = commands.getoutput('iostat -xNz')
		inDesiredSection = False
		for line in data:
			lineVals = string.split(line)
			if inDesiredSection and len(lineVals) > 0:
				#output is going to look like this:
				#Device: rrqm/s wrqm/s r/s w/s rkB/s wkB/s avgrq-sz avgqu-sz await r_await w_await  svctm  %util
				name = lineVals[0][:-1] #trim off the colon
				#saturation is the average queue size
				#rrqm = lineVals[1] #The number of read requests merged per second that were queued to the device.
				#wrqm = lineVals[2] #The number of write requests merged per second that were queued to the device.
				#r = lineVals[3] #The number of read requests that were issued to the device per second.
				#w = lineVals[4] #The number of write requests that were issued to the device per second.
				#rkB = lineVals[5] #The number of kilobytes read from the device per second.
				#wkB = lineVals[6] #The number of kilobytes written to the device per second.
				#avgrq = lineVals[7] #The average size (in sectors) of the requests that were issued to the device.
				avgqu = lineVals[8] #The average queue length of the requests that were issued to the device.
				#await = lineVals[9] #The average time (in milliseconds) for I/O requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
				#r_await = lineVals[10] #The average time (in milliseconds) for I/O read requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
				#w_await = lineVals[11] #The average time (in milliseconds) for I/O write requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them.
				#svctm = lineVals[12] #The average service time (in milliseconds) for I/O requests that were issued to the device. Warning! Do not trust this field any more. This field will be removed in a future sysstat version.
				util = lineVals[13] #Percentage of CPU time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this value is close to 100%.

				self.fieldValues[name + '_average_queue_size'] = avgqu
				self.fieldValues[name + '_percent_cpu_io_requests'] = util

			elif len(lineVals) > 0 and 'Device:' == lineVals[0]:
				inDesiredSection = True

class systemMonitorStorageCapacityUtilization(systemMonitor):
	def __init__(self):
		systemMonitor.__init__(self)

	def update(self):
		partitions = psutil.disk_partitions()
		
		#all=False means only return physical devices
		#all=True  means return al partitions including mempry partitions like /dev/shm
		for part in psutil.disk_partitions(all=True):
			name = part.device

			self.fieldValues[name + "_MountPoint"] = part.mountpoint
			self.fieldValues[name + "_fstype"] = part.fstype
			self.fieldValues[name + "_opts"] = part.opts

			usage = psutil.disk_usage(part.mountpoint)

			self.fieldValues[name + "_Total"] = usage.total
			self.fieldValues[name + "_Used"] = usage.total
			self.fieldValues[name + "_Free"] = usage.total
			self.fieldValues[name + "_Percent"] = usage.total
