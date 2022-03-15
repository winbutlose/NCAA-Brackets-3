from asyncio.windows_events import NULL
import pymongo
import json
import sys
from pymongo import MongoClient, InsertOne

if not len(sys.argv) == 2:
    print("need single arg: json filename")
    exit(1)

client = MongoClient('localhost', 27017)
#print(client.list_database_names())
db = client["fivewordreviews"]
collection = db["ratings"]
requesting = []

with open(r"static/"+sys.argv[1]+".json") as f:
    content = f.read()
    myDict = json.loads(content)
    print(myDict)
    requesting.append(InsertOne(myDict))
result = collection.bulk_write(requesting)

cursor = collection.find({})
for document in cursor:
    print(document)

#I dont think the json data should be a list, then it will be saved as a single document in mongo
    #propose saving either individual files for each rating, or separate json objects in 1 document, 1 object for each rating

client.close()