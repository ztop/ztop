import psutil
import socket

collectors = {"cpu_percent": psutil.cpu_times_percent,
              "network_usage": psutil.net_io_counters}  # this is a counter; should replace with diff


def format_for_submission(name, values):
    points = [socket.getfqdn()]
    columns = ["host"]
    for field, value in zip(values._fields, values):  # assumes named tuple; we'll have to handle cases here or standardize output
        points.append(value)
        columns.append(field)

    return {"points": [points],
            "name": name,
            "columns": columns}
