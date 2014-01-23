package main 

import "fmt"
//import "io"
import "os"

type Monitor interface {
	Update() // nil
}


// Example of a monitor. We could potentially place these in other files

/* A monitor for all of the data found in /proc/:pid/stat
pid %d       (1) The process ID.
comm %s      (2) The filename of the executable, in parentheses. This is visible whether or not the executable is swapped out.
state %c     (3) One character from the string "RSDZTW" where R is running, S is sleeping in an interruptible wait, D is waiting in uninterruptible disk sleep, Z is zombie, T is traced or stopped (on a signal), and W is paging.
ppid %d      (4) The PID of the parent.
pgrp %d      (5) The process group ID of the process.
session %d   (6) The session ID of the process.
tty_nr %d    (7) The controlling terminal of the process. (The minor device number is contained in the combination of bits 31 to 20 and 7 to 0; the major device number is in bits 15 to 8.)
tpgid %d     (8) The ID of the foreground process group of the controlling terminal of the process.
flags %u     (9) The kernel flags word of the process. For bit meanings, see the PF_* defines in the Linux kernel source file include/linux/sched.h. Details depend on the kernel version.
minflt %lu   (10) The number of minor faults the process has made which have not required loading a memory page from disk.
cminflt %lu  (11) The number of minor faults that the process's waited-for children have made.
majflt %lu   (12) The number of major faults the process has made which have required loading a memory page from disk.
cmajflt %lu  (13) The number of major faults that the process's waited-for children have made.
utime %lu    (14) Amount of time that this process has been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)). This includes guest time, guest_time (time spent running a virtual CPU, see below), so that applications that are not aware of the guest time field do not lose that time from their calculations.
stime %lu    (15) Amount of time that this process has been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).
cutime %ld   (16) Amount of time that this process's waited-for children have been scheduled in user mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)). (See also times(2).) This includes guest time, cguest_time (time spent running a virtual CPU, see below).
cstime %ld   (17) Amount of time that this process's waited-for children have been scheduled in kernel mode, measured in clock ticks (divide by sysconf(_SC_CLK_TCK)).
priority %ld (18) (Explanation for Linux 2.6) For processes running a real-time scheduling policy (policy below; see sched_setscheduler(2)), this is the negated scheduling priority, minus one; that is, a number in the range -2 to -100, corresponding to real-time priorities 1 to 99. For processes running under a non-real-time scheduling policy, this is the raw nice value (setpriority(2)) as represented in the kernel. The kernel stores nice values as numbers in the range 0 (high) to 39 (low), corresponding to the user-visible nice range of -20 to 19.
*/

// TODO: http://golang.org/ref/spec#Struct_types
// potentially we could include the friendly name as a tag to the end of the field
type ProcPidStat struct {
	pid       string
	comm      string
	state     string
	ppid      string
	pgrp      string
	session   string
	tty_nr    string
	tpgid     string
	flags     string
	minflt    string
	cminflt   string
	majflt    string
	cmajflt   string
	utime     string
	stime     string
	cutime    string
	cstime    string
	priority  string
	// ppid      int32
	// pgrp      int32
	// session   int32
	// tty_nr    int32
	// tpgid     int32
	// flags     uint32
	// minflt    uint64
	// cminflt   uint64
	// majflt    uint64
	// cmajflt   uint64
	// utime     uint64
	// stime     uint64
	// cutime    int64
	// cstime    int64
	// priority  int64
	// blah blah lots more fields
}

func (p *ProcPidStat) Update() {
	fi, err := os.Open(fmt.Sprintf("/proc/%s/stat", p.pid))
    if err != nil {
    	panic(err) 
    }
	// In Go, all int values are read with %d :p
	_, err = fmt.Fscanf(fi, "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s", 
		&p.pid, &p.comm, &p.state, &p.ppid, &p.pgrp, &p.session, &p.tty_nr, &p.tpgid, &p.flags, 
		&p.minflt, &p.cminflt, &p.majflt, &p.cmajflt, &p.utime, &p.stime, &p.cutime, &p.cstime, &p.priority)
    if err != nil {
    	panic(err) 
    }
}