import psutil
from systemMonitor import *

def convert_data_for_db_simple(dual_list):
    fields = []
    data = []
    for field, point in dual_list:
        data.append(point)
        fields.append(field)

    return fields, [data]

def process_generic_monitor(className):
    monitor = className()
    monitor.update()
    return convert_data_for_db_simple(monitor.fieldValues.iteritems())

def cpu_percent():
    values = psutil.cpu_times_percent()
    return convert_data_for_db_simple(zip(values._fields, values))

def network_usage():
    values = psutil.net_io_counters()

    fields = []
    data = []

    for field, point, last_point in zip(values._fields, values, network_usage.last_values):
        diff = point-last_point # doesn't handle overflow
        data.append(diff)
        fields.append(field)

    network_usage.last_values = values

    return fields, [data] # this data point doesn't have multiple rows; wrap in another
network_usage.last_values = []


def mem_info():
    return process_generic_monitor(systemMonitorMemInfo)

def networkUtilization():
    return process_generic_monitor(systemMonitorNetworkUtilization)

def cpu_utilization():
    return process_generic_monitor(systemMonitorCPUUtilization)

def cpu_saturation():
    return process_generic_monitor(systemMonitorCPUSaturation)

def cpu_errors():
    print "Not implemented"

def memory_capacity_utilization():
    return process_generic_monitor(systemMonitorMemoryCapacityUtilization)

def memory_capacity_saturation():
    return process_generic_monitor(systemMonitorMemoryCapacitySaturization)

def memory_capacity_errors():
    print "Not implemented"

def network_interfaces_utilization():
    print "Not implemented"

def network_interfaces_saturation():
    print "Not implemented"

def network_interfaces_errors():
    print "Not implemented"

def storage_device_io_utilization():
    print "Not implemented"

def storage_device_io_saturation():
    print "Not implemented"

def storage_device_io_errors():
    print "Not implemented"

def storage_capacity_utilization():
    print "Not implemented"

def storage_capacity_saturation():
    print "Not implemented"

def storage_capacity_errors():
    print "Not implemented"

def storage_controller_utilization():
    print "Not implemented"

def storage_controller_saturation():
    print "Not implemented"

def storage_controller_errors():
    print "Not implemented"

def network_controller_utilization():
    print "Not implemented"

def network_controller_saturation():
    print "Not implemented"

def network_controller_errors():
    print "Not implemented"

collectors = {"cpu_percent": cpu_percent,
              "network_usage": network_usage,
              "mem_info": mem_info,
              "net_dev": networkUtilization,
              "cpu_utilization": cpu_utilization,
              "cpu_saturation": cpu_saturation,
              #"cpu_errors": cpu_errors, #requres perf
              "memory_capacity_utilization": memory_capacity_utilization,
              "memory_capacity_saturation": memory_capacity_saturation
              #"memory_capacity_errors": memory_capacity_errors,
              #"network_interfaces_utilization": network_interfaces_utilization,
              #"network_interfaces_saturation": network_interfaces_saturation,
              #"network_interfaces_errors": network_interfaces_errors,
              #"storage_device_io_utilization": storage_device_io_utilization,
              #"storage_device_io_saturation": storage_device_io_saturation,
              #"storage_device_io_errors": storage_device_io_errors,
              #"storage_capacity_utilization": storage_capacity_utilization,
              #"storage_capacity_saturation": storage_capacity_saturation,
              #"storage_capacity_errors": storage_capacity_errors,
              #"storage_controller_utilization": storage_controller_utilization,
              #"storage_controller_saturation": storage_controller_saturation,
              #"storage_controller_errors": storage_controller_errors,
              #"network_controller_utilization": network_controller_utilization,
              #"network_controller_saturation": network_controller_saturation,
              #"network_controller_errors": network_controller_errors,
              #"cpu_interconnect_utilization": cpu_interconnect_utilization, #requires perf
              #"cpu_interconnect_saturation": cpu_interconnect_saturation,  #requires perf
              #"cpu_interconnect_errors": cpu_interconnect_errors,  #requires perf
              #"memory_interconnect_utilization": memory_interconnect_utilization,  #requires perf
              #"memory_interconnect_saturation": memory_interconnect_saturation,  #requires perf
              #"memory_interconnect_errors": memory_interconnect_errors,  #requires perf
              #"io_interconnect_utilization": io_interconnect_utilization,  #requires perf
              #"io_interconnect_saturation": io_interconnect_saturation,  #requires perf
              #"io_interconnect_errors": io_interconnect_errors,  #requires perf
              }
