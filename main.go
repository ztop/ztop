package main

import "fmt"
import "io/ioutil"
//import "os"
import "time"
import "strings"
import "strconv"
import "reflect"

func UpdateProcesses(plist map[string]*Process, fields *Fields) {
	fmt.Println("Current Process state")
	for _, v := range fields.names {
		fmt.Printf("%-20s", v)
	}
	fmt.Print("\n")

	procs, err := ioutil.ReadDir("/proc/")
	if err != nil {
		panic(err)
	}
	// range returns index, element
	for _, procfile := range procs {
		if procfile.IsDir()  {
			// we only want the processes :p
			name := procfile.Name()
    		_, err := strconv.Atoi(name)
    		if err == nil {
				process, present := plist[name]
				if present {
					// if the fields has changed since the last update
					// we want to edit the fields captured for this process
					process.Update()
				} else {
					process = new(Process)
					process.pid = name
					process.fields = make(map[string]*string)
					process.type_monitor = make(map[reflect.Type]*Monitor)
					process.AddFields(fields.names)
					process.Update()
					plist[name] = process
				}
				data := process.Data(fields.names)
				for _, v := range data {
					fmt.Printf("%-20s", v)
				}
				fmt.Print("\n")
			}		
		}
	}
	// set the fields parameter's update flag to false saying that I am done updating all the processes fields
	fields.update = false
}

type Fields struct {
	// flag to say if the list of fields has changed
	update bool
	// flag if a new field was added, true else a field was removed and this is false
	added []string
	// which field was added or removed
	removed []string
	// list of all the fields (needed for newly spawned processes)
	names []string
}

func IndexOfString(s []string, value string) int {
    for p, v := range s {
        if (v == value) {
            return p
        }
    }
    return -1
}

func (f *Fields) AddField(name string) {
	// TODO: verify that this is a possible field to add BEFORE adding it here
	f.update = true
	f.added = append(f.added, name)
	f.names = append(f.names, name)
}

func (f *Fields) RemoveField(name string) {
	index := IndexOfString(f.names, name)
	if index == -1 {
		// cannot remove a field that isn't here so just return
		return
	}
	f.update = true
	f.removed = append(f.removed, name)
	// some idomatic Go magic to remove an item
	f.names = f.names[:index+copy(f.names[index:], f.names[index+1:])]
}

func main() {
	// for each of the processes, make a Process struct and 
	// call update on it and print out the data about

	// update command to be sent every second
	ticker := time.NewTicker(1 * time.Second)
	quit := make(chan struct{})
	addfield := make(chan string)
	removefield := make(chan string)
	// spin off a gorountine for updateProcesses
	go func() {
		monitorFields := new(Fields)
		// simple default field to monitor for
		monitorFields.AddField("process_name")
		monitorFields.AddField("cpu_percent")

		// a list of processes where key is the process name 
		// and value is the process pointer
		processList := make(map[string]*Process)
		for {
			select {
			case <- ticker.C:
				UpdateProcesses(processList, monitorFields)
			case <- quit:
				ticker.Stop()
				return
			case <- addfield:
				monitorFields.AddField(<-addfield)
			case <- removefield:
				monitorFields.RemoveField(<-removefield)
			}
		}
	}()

	// wait for user input
	var input string = "test"
	for input != "done" {
		fmt.Scanln(&input)
		if strings.HasPrefix(input, "add ") {
			field := strings.TrimLeft(input, "add ")
			addfield <- field
		} else if strings.HasPrefix(input, "rem ") {
			field := strings.TrimLeft(input, "rem ")
			removefield <- field
		}
	}
	fmt.Println("Program Done")
	close(quit)
}