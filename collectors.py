import psutil
from systemMonitor import systemMonitorMemInfo

def cpu_percent():
    values = psutil.cpu_times_percent()

    fields = []
    data = []
    for field, point in zip(values._fields, values):
        data.append(point)
        fields.append(field)

    return fields, [data] # this data point doesn't have multiple rows; wrap in another

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
    memInfo = systemMonitorMemInfo()
    memInfo.update()
    keys = memInfo.fieldValues.keys()
    values = memInfo.fieldValues.values()

    fields = []
    data = []

    for field, point in memInfo.fieldValues.iteritems():
        data.append(point)
        fields.append(field)

    return fields, [data]


collectors = {"cpu_percent": cpu_percent,
              "network_usage": network_usage,
              "mem_info": mem_info}
