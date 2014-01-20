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
CPUTime* read_cpu_time(int proc_id, CPUTime *time_s) {
	int err;
	FILE * file;
	char * buf;
	sprintf(filename, STAT_FILE, proc_id);
	file = fopen(filename, "r");

	if (!file) {
		return NULL;
	}

	// file is open
	if (time_s == NULL) {
		time_s = malloc(sizeof(CPUTime));
		if (time_s == NULL){
			// malloc failed (out of memory)
			return NULL;
		}
	}
/*
(1) The process ID.
(2) The filename of the executable, in parentheses. This is visible whether or not the executable is swapped out.
(3) One character from the string "RSDZTW" where R is running, S is sleeping in an interruptible wait, D is waiting in uninterruptible disk sleep, Z is zombie, T is traced or stopped (on a signal), and W is paging.
(4) The PID of the parent.
(5) The process group ID of the process.
(6) The session ID of the process.
(7) The controlling terminal of the process. (The minor device number is contained in the combination of bits 31 to 20 and 7 to 0; the major device number is in bits 15 to 8.)
(8) The ID of the foreground process group of the controlling terminal of the process.
(9) The kernel flags word of the process. For bit meanings, see the PF_* defines in the Linux kernel source file include/linux/sched.h. Details depend on the kernel version.

minflt %lu
(10) The number of minor faults the process has made which have not required loading a memory page from disk.

cminflt %lu

(11) The number of minor faults that the process's waited-for children have made.

majflt %lu

(12) The number of major faults the process has made which have required loading a memory page from disk.

cmajflt %lu

(13) The number of major faults that the process's waited-for children have made.

utime %lu

(14) Amount of time that this process has been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)). This includes guest time, guest_time (time spent running a virtual CPU, see below), so that applications that are not aware of the guest time field do not lose that time from their calculations.

stime %lu

(15) Amount of time that this process has been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).

cutime %ld

(16) Amount of time that this process's waited-for children have been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)). (See also times(2).) This includes guest time, cguest_time (time spent running a virtual CPU, see below).

cstime %ld

(17) Amount of time that this process's waited-for children have been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).

priority %ld
*/

	// TODO: finish making this giant formatting string for reading in the proc file
	fscanf(file, "%d* %s* %c* %d* %d* %d* %d* %d* %u*")


f_error: // if I am unable to read the proc stat, then I need to close the file descriptor and clean up
	fclose(file);
}