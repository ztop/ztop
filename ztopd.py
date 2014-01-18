#!/usr/bin/python
import os
import sys

if os.name != 'posix':
    sys.exit('platform not supported')

import psutil
import socket
import time

from influxdb import client as influxdb
db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "ztop")


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


def pub_data(data):
    # later on, pub, with optional writing to db? or should the db be subbed?
    db.write_points(data)


def main():
    interval = 1
    while True:
        start_time = time.time()
        data = []
        for name, fn in collectors.iteritems():
            raw_data = fn()
            data.append(format_for_submission(name, raw_data))
        pub_data(data)
        while (start_time + interval - time.time()) > 0:
            rest_duration = start_time + interval - time.time()
            time.sleep(rest_duration)


if __name__ == '__main__':
    main()
