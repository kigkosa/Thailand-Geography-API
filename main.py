from fastapi import FastAPI
import pymongo


import requests
import json

app = FastAPI()


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["thailand_geography"]





@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/update_data")
async def root():
    client.drop_database('thailand_geography')
    update_json_to_mongodb("districts","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/districts.json")
    update_json_to_mongodb("provinces","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/provinces.json")
    update_json_to_mongodb("subdistricts","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/subdistricts.json")
    update_json_to_mongodb("geography","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/geography.json")
    return "ok"


def update_json_to_mongodb(db_name,url):
    collection = db[db_name]

    # Download JSON data from URL
    response = requests.get(url)

    # Parse JSON data
    data = json.loads(response.text)

    # Insert data into MongoDB
    collection.insert_many(data)
