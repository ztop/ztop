import socket

try:
    from influxdb import client as influxdb
    db = influxdb.InfluxDBClient("localhost", 8086, "root", "root", "ztop")
except:
    pass

def format_for_submission(table_name, columns, values):
    """formats data for submission into influxdb; 
    table_name: string for the table to submit into
    columns: array of strings with column names
    values: array of arrays with data following the specified columns.
    """
    columns.append("host")
    fqdn = socket.getfqdn()    

    for vrow in values:
        vrow.append(fqdn)

    return {"points": values,
            "name": table_name,
            "columns": columns}

def pub_data(data):
    """push to destination; for now, fall back to stdout if influxdb isn't installed"""
    if 'db' in vars() or 'db' in globals():
        db.write_points(data)
    else:
        import pprint
        pprint.pprint(data)
