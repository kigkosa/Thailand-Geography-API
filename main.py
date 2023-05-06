from fastapi import FastAPI
import pymongo


import requests
import json


import uvicorn

app = FastAPI(title="THAILAND GEOGRAPHY API",version="beta",description="ดึงค่าจังหวัดอำเภอตำบลฟรี",docs_url="/")


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["thailand_geography"]


def get_geographys(keyword,id):
    collection = db["geography"]
    _q = collection.find({id:  { "$regex": "^"+keyword+".*", "$options": "i" }})
    _subdistricts  = {}
    _x_id = 0
    for q in _q:
        _x_id +=1
        _subdistricts[_x_id] = {
            "provinceCode":q["provinceCode"],
            "subdistrictNameEn":q["subdistrictNameEn"],
            "subdistrictNameTh":q["subdistrictNameTh"],
            "districtNameEn":q["districtNameEn"],
            "districtNameTh":q["districtNameTh"],
            "provinceNameEn":q["provinceNameEn"],
            "provinceNameTh":q["provinceNameTh"],
            "postalCode":q["postalCode"],
            "districtCode":q["districtCode"],
            "subdistrictCode":q["subdistrictCode"],
            "postalCode":q["postalCode"]
            }
    _subdistricts["length"] = _x_id
    return _subdistricts
   

# Th
@app.get("/get_geographys/subdistrictNameTh",tags=["ค้นหาทั่งหมด"])
async def ดึงข้อมูลจากทั่งหมดตำบล(keyword):
    return get_geographys(keyword,"subdistrictNameTh")
@app.get("/get_geographys/districtNameTh",tags=["ค้นหาทั่งหมด"])
async def ดึงข้อมูลจากทั่งหมดจากอำเภอ(keyword):
    return get_geographys(keyword,"districtNameTh")
@app.get("/get_geographys/provinceNameTh",tags=["ค้นหาทั่งหมด"])
async def ดึงข้อมูลจากทั่งหมดจากจังหวัด(keyword):
    return get_geographys(keyword,"provinceNameTh")

# En
@app.get("/get_geographys/subdistrictNameEn",tags=["ค้นหาทั่งหมด"])
async def ดึงข้อมูลจากทั่งหมดตำบลภาษาอังกฤษ(keyword):
    return get_geographys(keyword,"subdistrictNameEn")
@app.get("/get_geographys/districtNameEn",tags=["ค้นหาทั่งหมด"])
async def ดึงข้อมูลจากทั่งหมดจากอำเภอภาษาอังกฤษ(keyword):
    return get_geographys(keyword,"districtNameEn")
@app.get("/get_geographys/provinceNameEn",tags=["ค้นหาทั่งหมด"])
async def ดึงข้อมูลจากทั่งหมดจากจังหวัดภาษาอังกฤษ(keyword):
    return get_geographys(keyword,"provinceNameEn")


@app.get("/get_subdistricts",tags=["ค้นหาเฉพาะ"])
async def ดึงข้อมูลจากตำบล(keyword):
    collection = db["subdistricts"]
    _q = collection.find({"subdistrictNameTh":  { "$regex": "^"+keyword+".*", "$options": "i" }})
    _subdistricts  = {}
    _x_id = 0
    for q in _q:
        _x_id +=1
        _subdistricts[_x_id] = {
            "provinceCode":q["provinceCode"],
            "subdistrictNameEn":q["subdistrictNameEn"],
            "subdistrictNameTh":q["subdistrictNameTh"],
            "postalCode":q["postalCode"],
            "districtCode":q["districtCode"],
            "subdistrictCode":q["subdistrictCode"],
            "postalCode":q["postalCode"]
            }
    _subdistricts["length"] = _x_id
    return _subdistricts



@app.get("/get_districts",tags=["ค้นหาเฉพาะ"])
async def ดึงข้อมูลจากอำเภอ(keyword):
    collection = db["districts"]
    _q = collection.find({"districtNameTh":  { "$regex": "^"+keyword+".*", "$options": "i" }})
    _districts  = {}
    _x_id = 0
    for q in _q:
        _x_id +=1
        _districts[_x_id] = {
            "provinceCode":q["provinceCode"],
            "districtNameEn":q["districtNameEn"],
            "districtNameTh":q["districtNameTh"],
            "postalCode":q["postalCode"],
            "districtCode":q["districtCode"]
            }
    _districts["length"] = _x_id
    return _districts




@app.get("/get_province",tags=["ค้นหาเฉพาะ"])
async def ดึงข้อมูลจากจังหวัด(keyword):
    collection = db["provinces"]
    _q = collection.find({"provinceNameTh":  { "$regex": "^"+keyword+".*", "$options": "i" }})
    _province  = {}
    _x_id = 0
    for q in _q:
        _x_id +=1
        _province[_x_id] = {
            "provinceCode":q["provinceCode"],
            "provinceNameEn":q["provinceNameEn"],
            "provinceNameTh":q["provinceNameTh"]
            }
    _province["length"] = _x_id
    return _province


@app.get("/update_data",tags=["อัพเดทฐานข้อมูล"])
async def อัพเดทข้อมูลทั่งหมด():
    client.drop_database('thailand_geography')
    update_json_to_mongodb("districts","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/districts.json")
    update_json_to_mongodb("provinces","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/provinces.json")
    update_json_to_mongodb("subdistricts","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/subdistricts.json")
    update_json_to_mongodb("geography","https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/geography.json")
    return "Update data"


def update_json_to_mongodb(db_name,url):
    collection = db[db_name]

    # Download JSON data from URL
    response = requests.get(url)

    # Parse JSON data
    data = json.loads(response.text)

    # Insert data into MongoDB
    collection.insert_many(data)



    
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)