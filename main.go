package main

import "fmt"
import "io/ioutil"
//import "os"
import "time"

func updateProcesses(plist *[]Process) {
	procs, err := ioutil.ReadDir("/proc/")
	if err != nil {
		panic(err)
	}
	// range returns index, element
	for _, procfile := range procs {
		fmt.Println(procfile.Name())
	}
	// p := new(Process)  // type *Process
}

func main() {
	// for each of the processes, make a Process struct and 
	// call update on it and print out the data about 
	monitorFields := make([]string, 0)
	monitorFields = append(monitorFields, "cpu_percent")

	// update command to be sent every second
	ticker := time.NewTicker(1 * time.Second)
	quit := make(chan struct{})
	// spin off a gorountine for updateProcesses
	go func() {
		// TODO: I don't want to recreate this slice every time, just update it :p
		processList := make([]Process, 0)
		// which fields I want returned
		for {
			select {
			case <- ticker.C:
				updateProcesses(&processList)
			case <- quit:
				ticker.Stop()
				return
			// example of adding a new field
			//case <- newfield:
				//addField()
			}
		}
	}()

	// wait for user input
	var input string
	fmt.Scanln(&input)
	fmt.Println("done")
	close(quit)
}