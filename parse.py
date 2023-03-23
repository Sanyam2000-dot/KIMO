import json
import pymongo
import moment
import datetime
import time
from uuid import uuid4

with open('courses.json') as f:
  data = json.load(f)

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["KIMO"]
mycol = mydb["courses"]  

uuid_obj = uuid4()
print(uuid_obj)
# For unix timestamp 

 
# date_time = datetime.datetime(2023, 3, 13, 21, 20)
 

# print("date_time =>",date_time)
 

# print("unix_timestamp => ",
#       (time.mktime(date_time.timetuple())))

# mycol.update_one({"name" : "Big Data"}, {"$set":{"date" : (time.mktime(date_time.timetuple()))}})





for x in data:
    i = mycol.insert_one(x)


for y in mycol.find():
  print(y) 