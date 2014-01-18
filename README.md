ztop
====

linux data aggregator


Installation
===========

Long-term, we want configuration to be as minimal as possible. Right
now... not so much.

Install influxdb:
http://influxdb.org/download/

Install python library using setuptools
sudo pip install influxdb

./influxdb_setup.py # for now, just creates a ztop database

I had to manually upgrade my six (python 2/3 compatibility library);
if this is a common issue, we may want to include it in the repo; it
is contained in a [single file](https://pypi.python.org/pypi/six/)
(after extraction). Just put the file in the same directory as the
influxdb scripts.


Reading data from influxdb
==========================
http://influxdb.org/docs/api/http.html

You can explore with basic web interface at
localhost:8083. login with the cluster admin as root/root, and add a
db user. After user creation, connect as a database user to the ztop
database. Run a query like "select * from cpu_percent"

*the API uses port 8086
