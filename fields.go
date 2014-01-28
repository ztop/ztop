/*
This file contains the magical functions needed to look up which struct and which I need 
in order to collect the information for the field.
*/

package main

import (
	"reflect"
	"fmt"
)

// 
var field_mapping = map[string]string{
    "cpu_percent":  "utime",
    "process_name": "comm",
}

func FieldToStruct(name string) reflect.Type {
	// TODO: make this more dynamic lol
	if name == "cpu_percent" {
		var monitor_type = reflect.TypeOf((*ProcPidStat)(nil)).Elem()
		return monitor_type //, monitor_type.FieldByName(name)
	} else if name == "process_name" {
		return reflect.TypeOf((*ProcPidStat)(nil)).Elem()
	} else {
		fmt.Printf("name == %s\n", name)
		return nil 
	}
}

func FieldToStructField(name string) string {
	// TODO: make this more dynamic as well
	field, ok := field_mapping[name]
	if ok {
		return field
	} else {
		panic("Field not found")
	}

	// if name == "cpu_percent" {
	// 	var monitor_type = reflect.TypeOf((*ProcPidStat)(nil)).Elem()
	// 	field, _ := monitor_type.FieldByName("utime")
	// 	fmt.Println("Cpu Percentage")
	// 	return field
	// } else if name == "process_name" {
	// 	var monitor_type = reflect.TypeOf((*ProcPidStat)(nil)).Elem()
	// 	field, _ := monitor_type.FieldByName("comm")
	// 	fmt.Println("Process Name")
	// 	return field
	// } else {
	// 	var monitor_type = reflect.TypeOf((*ProcPidStat)(nil)).Elem()
	// 	field, _ := monitor_type.FieldByName("notfound")
	// 	fmt.Println("PANNIICCCCCC")
	// 	fmt.Printf("name == %s\n", name)
	// 	return field
	// }	
}
