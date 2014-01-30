#!/usr/bin/python

from influxdb import client as influxdb

db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "ztop")

try:
    db.delete_database("ztop")
except Exception as e:
    print(e)

try:
    db.create_database("ztop")
except Exception as e:
    print(e)

