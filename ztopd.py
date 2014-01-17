#!/usr/bin/python
from itertools import izip

import socket
from time import sleep

from influxdb import client as influxdb

db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "ztop")

import psutil

def collect_data():
    cpu_percent = psutil.cpu_times_percent(interval=1)
    data = format_for_submission("cpu_percent", cpu_percent)
    db.write_points([data])


def format_for_submission(name, values):
    points = [socket.getfqdn()]
    columns = ["host"]
    for field, value in izip(values._fields, values):
        points.append(value)
        columns.append(field)

    return {"points": [points],
            "name": name,
            "columns": columns}


while True:
    collect_data()
    sleep(1)
