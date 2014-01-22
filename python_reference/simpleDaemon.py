import os
import sys
if os.name != 'posix':
	sys.exit('platform not supported')

import time

import psutil
import json

def poll(interval):
	# sleep some time
	time.sleep(interval)
	procs = []
	procs_status = {}
	for p in psutil.process_iter():
		try:
			p.dict = p.as_dict(['username', 'nice',# 'memory_info',
								#'memory_percent', 'cpu_percent',
								#'cpu_times', 
								'name', 'status'])
			try:
				procs_status[p.dict['status']] += 1
			except KeyError:
				procs_status[p.dict['status']] = 1
		except psutil.NoSuchProcess:
			pass
		else:
			procs.append(p)

	# return processes sorted by CPU percent usage
	#processes = sorted(procs, key=lambda p: p.dict['cpu_percent'],reverse=True)
	processes = sorted(procs, key=lambda p: p.dict['status'],reverse=True)
	return (processes, procs_status)

def main():
	try:
		interval = 0
		while 1:
			processes, procs_status = poll(interval)
			for p in processes:
				print 'PROC:', p
			for stat in procs_status:
				print 'STAT:', stat
			interval = 1
	except (KeyboardInterrupt, SystemExit):
		pass

if __name__ == '__main__':
	main()