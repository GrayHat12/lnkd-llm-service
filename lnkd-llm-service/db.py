from pymongo import MongoClient

mongo_connection = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_connection["lnkd-llm"]

def lnkd_requests_collection():
    return mongo_db["lnkd_requests"]