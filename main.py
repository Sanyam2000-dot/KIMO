from typing import Union
import pymongo
from fastapi import FastAPI
import json
from bson import json_util
from bson.objectid import ObjectId
from pydantic import BaseModel

app = FastAPI()
client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["KIMO"]
mycol = mydb["courses"]


@app.get("/")
def read_root():
    return {"KIMO": "SWE ASSIGNMENT"}


def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.get("/allCourses")
async def read_item(date: int = 0,
                    name: int = 0,
                    rating: int = 0,
                    q: Union[str, None] = None):
    final = []
    sortArray = []
    if (date == 1):
        sortArray.append(("date", -1))
    if (name == 1):
        sortArray.append(("name", 1))
    if (rating == 1):
        sortArray.append(("courseRating", -1))

    if (sortArray != []):
        if (q):
            data = mycol.find({"domain": q}).sort(sortArray)
        else:
            data = mycol.find({}).sort(sortArray)
    else:
        if (q):
            data = mycol.find({"domain": q})
        else:
            data = mycol.find({})

    for x in data:
        final.append(x)
    print("here", final)
    a = parse_json(final)
    return {"Courses": a}


@app.get("/courseOverview")
def read_item(q: str):
    courseOverview = mycol.find_one({"_id": ObjectId(q)})
    a = parse_json(courseOverview)
    return {"courseOverview": a}


@app.get("/getChapterInformation")
def read_item(q: str):
    chapterInfo = mycol.aggregate([{
        "$match": {
            "chapters": {
                "$elemMatch": {
                    "chapterId": q
                }
            }
        }
    }, {
        "$project": {
            "chapter": "$chapters",
            "_id": 0
        }
    }])
    final = []
    a = parse_json(chapterInfo)
    print(a[0]['chapter'])
    for x in a[0]['chapter']:
        if (x['chapterId'] == str(q)):
            final.append(x)
    return {"chapterInfo": final}


class Rating(BaseModel):
    rating: int


@app.post("/rateCourse")
def read_item(coureseId, rating: Rating):
    courseRating = mycol.find_one_and_update(
        {"_id": ObjectId(coureseId)}, {"$set": {
            "courseRating": rating.rating
        }})
    return "Course Rated Successfully"
