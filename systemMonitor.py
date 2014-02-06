import string

class systemMonitorMemInfo():

	fieldValues = {}

	def __init__(self):
		fieldValues = {}

	def getFieldValue(self, name):
		result = self.fieldValues[name]
		if not result or result == '':
			result = 'no data'
		return result

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


class systemMonitorNetworkUtilization():
	fieldValues = {}

	def __init__(self):
		fieldValues = {}

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






class systemMonitorInterrupts():

	fieldValues = {}

	def __init__(self):
		fieldValues = {}

	def getFieldValue(self, interruptID):
		result = self.fieldValues[name]
		if not result or result == '':
			result = 'no data'
		return result;


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





def test():
	sysMon = systemMonitorMemInfo()
	sysMon.update()
	for key, value in sysMon.fieldValues.iteritems():
		print key, '\t\t', value

if __name__ == '__main__':
	test()



