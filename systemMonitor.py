import string
import os
import commands
import time

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


class systemMonitorNetworkUtilization(systemMonitor):

	def __init__(self):
		systemMonitor.__init__(self)

	#Interface refers to the name of the device we are looking at
	#receiveTransmit: 'receive' or 'transmit'
	#Column can be one of the following:
	#	bytes
	#	packets
	#	errs
	#	drop
	#	fifo
	#	compressed
	#	frame (receive only)
	#	multicast (receive only)
	#	colls (transmit only)
	#	carrier (transmit only) 
	def getFieldValue(self, interface, receiveTransmit, column):
		result = self.fieldValues[interface][isreceive][column]
		if not result or result == '':
			result = 'no data'
		return result;

	def update(self):
		infoFile = open('/proc/net/dev', 'r')
		if infoFile:
			firstLine = infoFile.readline()
			secondLine = infoFile.readline()
			majorheaders = string.split(secondLine, '|')
			majorheaders[0] = 'interface'
			receiveHeaders = string.split(majorheaders[1])
			transmitHeaders = string.split(majorheaders[2])

			for line in infoFile:
				receiveDictionary = {}
				transmitDictionary = {}
				valueDictionary = {'receive': receiveDictionary, 'transmit': transmitDictionary}
				
				values = string.split(line)
				interfaceName = values[0][:-1]

				self.fieldValues[interfaceName] = valueDictionary

				#received info
				index = 1
				for key in receiveHeaders:
					value = values[index]
					receiveDictionary[key] = value
					index = index + 1

				#transmit info
				for key in transmitHeaders:
					value = values[index]
					transmitDictionary[key] = value
					index = index + 1
			print self.fieldValues





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
				print line[:3]
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

class systemMonitorNetworkInterfacesUtilization(systemMonitor):
	def __init__(self):
		systemMonitor,__init__(self)

	def update(self):
		infoFile = open('/proc/net/dev', 'r')