package main 

import "fmt"
//import "io"
import "os"
//import "reflect"
import "bufio"
import "strings"

type SysMonitorMemInfo interface {
	GetPointer(string) *string
	Update() // nil
}

var fieldValues = map[string]string{
	"memtotal": 		"",
	"memfree": 			"",
	"buffers": 			"",
	"cached": 			"",
	"swapcached": 		"",
	"active": 			"",
	"inactive": 		"",
	"active_anon": 		"",
	"inactive_anon": 	"",
	"active_file": 		"",
	"inactive_file": 	"",
	"unevictable": 		"",
	"mlocked": 			"",
	"swaptotal": 		"",
	"swapfree": 		"",
	"dirty": 			"",
	"writeback": 		"",
	"anonpages": 		"",
	"mapped": 			"",
	"shmem": 			"",
	"slab": 			"",
	"sreclaimable": 	"",
	"sunreclaim": 		"",
	"kernelstack": 		"",
	"pagetables": 		"",
	"nfs_unstable": 	"",
	"bounce": 			"",
	"writebacktmp": 	"",
	"commitlimit": 		"",
	"committed_as": 	"",
	"vmalloctotal": 	"",
	"vmallocused": 		"",
	"vmallocchunk": 	"",
	"hardwarecorrupted":"",
	"anonhugepages": 	"",
	"hugepages_total": 	"",
	"hugepages_free": 	"",
	"hugepages_rsvd": 	"",
	"hugepages_surp": 	"",
	"hugepagesize": 	"",
	"directmap4k": 		"",
	"directmap2m": 		"",
	"BASE_RESULT":		"NOT FOUND"
}


// Example of a monitor. We could potentially place these in other files

/* A monitor for all of the data found in /proc/meminfo
MemTotal:			(1) Total memory allocated for the system
MemFree:			(2) Total memory available to allocate for the system
Buffers:			(3)
Cached:				(4)
SwapCached:			(5)
Active:				(6)
Inactive:			(7)
Active(anon):		(8)
Inactive(anon):		(9)
Active(file):		(10)
Inactive(file):		(11)
Unevictable:		(12)
Mlocked:			(13)
SwapTotal:			(14)
SwapFree:			(15)
Dirty:				(16)
Writeback:			(17)
AnonPages:			(18)
Mapped:				(19)
Shmem:				(20)
Slab:				(21)
SReclaimable:		(22)
SUnreclaim:			(23)
KernelStack:		(24)
PageTables:			(25)
NFS_Unstable:		(26)
Bounce:				(27)
WritebackTmp:		(28)
CommitLimit:		(29)
Committed_AS:		(30)
VmallocTotal:		(31)
VmallocUsed:		(32)
VmallocChunk:		(33)
HardwareCorrupted:	(34)
AnonHugePages:		(35)
HugePages_Total:	(36)
HugePages_Free:		(37)
HugePages_Rsvd:		(38)
HugePages_Surp:		(39)
Hugepagesize:		(40)
DirectMap4k:		(41)
DirectMap2M:		(42)

*/

// TODO: http://golang.org/ref/spec#Struct_types
// potentially we could include the friendly name as a tag to the end of the field
type MemInfoStat struct {
	memtotal			string
	memfree				string
	buffers				string
	cached				string
	swapcached			string
	active				string
	inactive			string
	active_anon			string
	inactive_anon		string
	active_file			string
	inactive_file		string
	unevictable			string
	mlocked				string
	swaptotal			string
	swapfree			string
	dirty				string
	writeback			string
	anonpages			string
	mapped				string
	shmem				string
	slab				string
	sreclaimable		string
	sunreclaim			string
	kernelstack			string
	pagetables			string
	nfs_unstable		string
	bounce				string
	writebacktmp		string
	commitlimit			string
	committed_as		string
	vmalloctotal		string
	vmallocused			string
	vmallocchunk		string
	hardwarecorrupted	string
	anonhugepages		string
	hugepages_total		string
	hugepages_free		string
	hugepages_rsvd		string
	hugepages_surp		string
	hugepagesize		string
	directmap4k			string
	directmap2m			string
}

func (p *MemInfoStat) GetPointer(name string) *string {
	// I couldn't find a fancy Reflect way to do this so the is the best I get
	
	result = fieldValues[name]
	if result == "" {
		result = fieldValues["BASE_RESULT"]
	}
	return &result
}

func (p *MemInfoStat) Update() {
	fi, err := os.Open("/proc/meminfo")
	if err != nil {
		panic(err) 
	}
	//The file has each value separated by line
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		//Of the format 
		//Name:        Int kB
		string[] strings = split(scanner.Text(), ", ")
		fieldValues[strings[0]] = strings[1] + strings[2]
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "Parsing values from /proc/meminfo:", err)
	}
	fi.Close()
}