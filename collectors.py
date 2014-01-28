import psutil

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


collectors = {"cpu_percent": cpu_percent,
              "network_usage": network_usage}
