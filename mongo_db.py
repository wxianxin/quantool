import datetime
import pandas as pd
import pymongo

# Connection URL
# Replace 'localhost' with the IP or hostname of your MongoDB server if it's remote
# Include the port if it's not the default port 27017
# Example for remote MongoDB: "mongodb://username:password@host:port/"
username = ""
password = ""
mongodb_uri = f"mongodb://{username}:{password}@192.168.8.8:27017/"
client = pymongo.MongoClient(mongodb_uri)

# Database Name
db = client["mydatabase"]

# Collection Name
collection = db["mycollection"]

# Inserting a document into the collection
collection.insert_one({"name": "John", "age": 30, "city": "New York"})
collection.insert_one({"name": "s", "age": 32, "city": "New"})

# Querying for a single document
user = collection.find_one({"name": "John"})
print(user)

query = {"age": {"$gt": 25}}
documents = collection.find(query)
for doc in documents:
    print(doc)

# Find documents where "age" is greater than 25 and "name" is "John"
query = {"$and": [{"age": {"$gt": 25}}, {"name": "s"}]}
documents = collection.find(query)
for doc in documents:
    print(doc)

# Optional: Close the connection
client.close()


############################################################################################################
# time series data

db.create_collection(
    name="ts_collection",
    timeseries={
        "timeField": "timestamp",
        "metaField": "trading_pair",  # optional
        "granularity": "seconds",
    },
)

collection = db["ts_collection"]

data = {
    "timestamp": [
        datetime.datetime(2024, 1, 1, 12, 0, 0, 1000),  # 1ms
        datetime.datetime(2024, 1, 1, 12, 0, 0, 2000),  # 2ms
        datetime.datetime(2024, 1, 1, 12, 0, 0, 3000),  # 3ms
    ],
    "value": [10, 20, 30],
    "timestamp_ms": [
        int(datetime.datetime.now().timestamp() * 1e6),
        int(datetime.datetime.now().timestamp() * 1e6),
        int(datetime.datetime.now().timestamp() * 1e6),
    ],
    "metadata": ["sensor1", "sensor2", "sensor3"],
}
df = pd.DataFrame(data)
records = df.to_dict("records")
collection.insert_many(records)
