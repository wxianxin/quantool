from pymongo import MongoClient

# Connection URL
# Replace 'localhost' with the IP or hostname of your MongoDB server if it's remote
# Include the port if it's not the default port 27017
# Example for remote MongoDB: "mongodb://username:password@host:port/"
client = MongoClient("mongodb://username:password@192.168.8.8:27017/")

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
