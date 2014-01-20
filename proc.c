#include "proc.h"
#include <stdio.h>
#include <errno.h>
#include <string.h>

// the stat_file for a single process
const char[] STAT_FILE = "/proc/%d/stat";
// using 20 as a rough estimate of the final size of the string to avoid 
// having to realloc the pointer and avoid other caluclations.
char *filename = malloc(sizeof(char) * 20);

/*
reads the CPU time for the process identified by the proc_id parameter
Parameters: 
proc_id = the process id to stat
CPU_time = the struct to update. This struct will also be the return value. If this is null, malloc a new one.

Returns: 
CPU_time if the process was able to be stated otherwise null. 

TODO: Maybe make the function take in an optional FILE descriptor
*/
CPUTime* read_cpu_time(int proc_id, CPUTime *time) {
	int err;
	FILE * file;
	sprintf(filename, STAT_FILE, proc_id);
	file = fopen(filename, "r");

	if (!file) {
		return NULL;
	}


f_error: // if I am unable to read the proc stat, then I need to close the file descriptor and clean up
	fclose(file);
}