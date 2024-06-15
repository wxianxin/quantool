# pip3 install influxdb-client

# ini client
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = os.environ.get("INFLUXDB_TOKEN")
org = "RocketStar"
url = "http://192.168.8.8:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# write data
bucket = "rs_bucket"

write_api = client.write_api(write_options=SYNCHRONOUS)

# for value in range(5):
#     point = Point("measurement1").tag("tagname1", "tagvalue1").field("field1", value)
#     write_api.write(bucket=bucket, org="RocketStar", record=point)
#     time.sleep(1)  # separate points by 1 second

# query data
query_api = client.query_api()

query = """from(bucket: "rs_bucket")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
query = "select * from measurement1"
tables = query_api.query(query, org="RocketStar")

for table in tables:
    for record in table.records:
        print(record)

# Aggregate Query
