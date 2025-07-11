from pymongo import MongoClient

client=MongoClient("mongodb+srv://hemanths1ga21cs066:HSZaq10plM@cluster0.dqknlk3.mongodb.net/")
mongo_db=client["machine_status"]
machine_collection=mongo_db["status"]