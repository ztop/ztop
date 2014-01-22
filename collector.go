package main

//import "fmt"
//import "reflect"

type Process struct {
	pid uint
	// slice of all the struct fields from where we want to return values
	// the key is the struct which has the field we wanna return data from
	// the value is the list of names of struct fields to return data about
	fields map[*Monitor][]string//reflect.StructField
}

func (p Process) removeField(struct_name string, field string) {
	// removes the field from the list of fields to monitor
	// if there are no more StructFields to 
}

func (p Process) addField(struct_name string, field string) {
	// adds a struct field to the list of visible
	// accomplishes this by checking the map for struct_name 
	// and then checks the struct for the field and adds that field 
	// to the slice of StructFields
	// if there is not monitor in the map for the requested field,
	// look up the monitor required to monitor this stat and add it
}

func (p Process) update() {
	// calls update on each of the monitors in the map. If the addField
	// and removeField are working as intended, then this should only
	// poll data from just the sources required
}