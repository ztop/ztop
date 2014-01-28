import socket

from influxdb import client as influxdb
db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "ztop")


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
