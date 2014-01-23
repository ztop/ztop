package main

import "fmt"
import "reflect"

type Process struct {
	pid string
	// monitors is all of the locations that we will need to derive data from
	monitors []Monitor
	// A map of all the types to a pointer to the monitor
	type_monitor map[reflect.Type]*Monitor
	fields map[string]*Monitor//reflect.StructField //, reflect.Type)
}

func (p *Process) RemoveField(field string) {
	// removes the field from the list of fields to monitor
	// if there are no more fields left in that monitor, then we can 
	// remove that monitor from the fields. (That way we don't have to check it anymore)
}

func (p *Process) AddField(field string) {
	// find the struct that this field belongs to
	monitor_type := FieldToStruct(field)
	monitor, exists := p.type_monitor[monitor_type]
	if !exists {
		// If there isn't a monitor for this field, make a new monitor
		monitor := reflect.New(monitor_type).Interface().(Monitor)
		p.monitors = append(p.monitors, monitor)
		p.type_monitor[monitor_type] = &monitor
	}
	p.fields[field] = monitor
}

func (p *Process) AddFields(fields []string) {
	// TODO: Make a more intelligent way of reversing struct names from fields that I want
	// TODO: See fields.go for more info

	// This method should be called by new Processes that need to add in all the 
	// current fields that we are monitoring
	for _, v := range fields {
		p.AddField(v)
	}
}

func (p *Process) Update() {
	// calls update on each of the monitors in the map. If the addField
	// and removeField are working as intended, then this should only
	// poll data from just the sources required
	for _, v := range p.monitors {
		v.Update()
	}
}

func (p *Process) Data(fields []string) []string {
	// returns a list of all the data collected in the order provided by fields
	// Potentially, we could change this to be a dynamic struct of just the
	// values that we need to return.
	ret := make([]string, len(fields))
		fmt.Println(fields)
		fmt.Println(p.fields)
	for i, field := range fields {
		monitor := p.fields[field]
		name := FieldToStructField(field)
		f_type := reflect.ValueOf(monitor).FieldByName(name)
		ret[i] = fmt.Sprintf("%d", f_type.String())
	}
	return ret
}