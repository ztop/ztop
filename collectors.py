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



collectors = {"cpu_percent": [cpu_percent],
              "mem_info": [process_generic_monitor, systemMonitorMemInfo],
              "cpu_utilization": [process_generic_monitor, systemMonitorCPUUtilization],
              "cpu_saturation": [process_generic_monitor, systemMonitorCPUSaturation],
              #"cpu_errors": cpu_errors, #requres perf
              "memory_capacity_utilization": [process_generic_monitor, systemMonitorMemoryCapacityUtilization],
              "memory_capacity_saturation": [process_generic_monitor, systemMonitorMemoryCapacitySaturization],
              #"memory_capacity_errors": memory_capacity_errors,
              "network_interfaces_utilization": [network_usage],
              #"network_interfaces_saturation": network_interfaces_saturation, #information grabbed in network usage call
              #"network_interfaces_errors": network_interfaces_errors,          #information grabbed in network usage call
              "storage_device_io_utilization": [process_generic_monitor, systemMonitorStorageDeviceIOUtilization],
              "storage_device_io_saturation": [process_generic_monitor, systemMonitorStorageDeviceIOSaturation],
              #"storage_device_io_errors": storage_device_io_errors,
              "storage_capacity_utilization": [process_generic_monitor, systemMonitorStorageCapacityUtilization],
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
