# pip install influxdb-client # v2
# pip install influxdb3-python
# support: writing, writing from file, querying, Apache Arrow(e.g. Pandas, Numpy)

# reference: https://github.com/InfluxCommunity/influxdb3-python/blob/main/Examples/pokemon-trainer/cookbook.ipynb
############################################################################################################

# import datetime
import random
import pandas as pd
from influxdb_client_3 import (
    InfluxDBClient3,
    InfluxDBError,
    WriteOptions,
    write_client_options,
    # Point,
)

# Initialization
host = "http://192.168.8.8:8086"
org = "RocketStar"
token = ""
database = "measurement1"


############################################################################################################
# This class handles the callbacks for the batching
class BatchingCallback(object):
    def success(self, conf, data: str):
        print(f"Written batch: {conf}")

    def error(self, conf, data: str, exception: InfluxDBError):
        print(f"Cannot write batch: {conf}, data: {data} due: {exception}")

    def retry(self, conf, data: str, exception: InfluxDBError):
        print(
            f"Retryable error occurs for batch: {conf}, data: {data} retry: {exception}"
        )


callback = BatchingCallback()

# This is the configuration for the batching. This is wrapped in a WriteOptions object. Within this example you
# can see the different options that can be set for the batching.
# Batch size is the number of points to write before the batch is written to the server.
# Flush interval is the time in milliseconds to wait before the batch is written to the server.
# Jitter interval is the time in milliseconds to wait before the batch is written to the server.
# Retry interval is the time in milliseconds to wait before retrying a failed batch.
# Max retries is the maximum number of times to retry a failed batch.
# exponential base is the base for the exponential retry delay.
write_options = WriteOptions(
    batch_size=100,
    flush_interval=10_000,
    jitter_interval=2_000,
    retry_interval=5_000,
    max_retries=5,
    max_retry_delay=30_000,
    exponential_base=2,
)


# This is the configuration for the write client. This is wrapped in a WriteClientOptions object.
# As you can see we incldue the BatchingCallback object we created earlier, plus the write_options.
wco = write_client_options(
    success_callback=callback.success,
    error_callback=callback.error,
    retry_callback=callback.retry,
    write_options=write_options,
)

############################################################################################################
client = InfluxDBClient3(
    token=token,
    host=host,
    org=org,
    database=database,
    enable_gzip=True,
    write_client_options=wco,
)
############################################################################################################
# create data
df = pd.DataFrame(
    {
        "time": pd.date_range(start="2024-01-01", periods=100, freq="s"),
        "tag1": "tag1",
        "tag2": "tag2",
        "value": random.sample(range(100), 100),
    }
)
############################################################################################################
# Write data
# data = Point().tag().field().field().time()
# client.write(data)
try:
    client.write(
        bucket="rs_db",
        data=df,
        data_frame_measurement_name="measurement1",  # measurement is basically table in influxdb
        data_frame_tag_columns=[
            "tag1",
            "tag2",
        ],  #  tags are parts of primary key in influxdb
    )
except InfluxDBError as e:
    print(f"InfluxDBError writing data: {e}")
except Exception as e:
    print(f"Error writing data: {e}")
############################################################################################################
# query data
sql = """
    SHOW COLUMNS FROM measurement1
    """
sql = """
    SELECT * FROM measurement1
    """

table = client.query(
    query=sql,
    language="sql",
    mode="pandas",
    # database="rs_db",
)

df = table.to_pandas()

############################################################################################################
# parquet read/write
import pyarrow.parquet as pq

pq.write_table(table, "table.parquet")
table = pq.read_table("table.parquet")
client.write_file(
    "table.parquet",
    measurement_name="measurement1",
    database="rs_db",
    time_column="time",
    tag_columns=["tag1", "tag2"],
)


############################################################################################################
# read large data, use "chunk" mode
sql = """
    SELECT * FROM measurement1
    """
table = client.query(query=sql, language="sql", mode="chunk", chunk_size=1000)
for chunk in table:
    print(chunk)
    # do something with the chunk
