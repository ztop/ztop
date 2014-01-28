from influxdb import client as influxdb
db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "ztop")

def pub_data(data):
    # later on, pub, with optional writing to db? or should the db be subbed?
    db.write_points(data)
