import pandas as pd
from pymongo import MongoClient

#connecting MongoDB-Database and creating a collection
conn = MongoClient("mongodb://localhost:27017/")
db = conn["snscrape_data"]
coll = db["twitter"]
for each in coll.find():
    print(each)