#ifndef _PROC__H
#define _PROC__H

// Data regarding the CPU Time usage for a single process
typedef struct _cpu_time {
	
} CPUTime;

typedef struct _network_usage {
	
} NetworkUsage;

// Contains the data about a single process
typedef struct _monitor {
	CPUTime *CPU_time;
	NetworkUsage *network_usage;
} Monitor;

// Updates all of the fields for this monitor
void update(Monitor*);

#endif