from pymongo import MongoClient
from ulid import ULID

mongo_connection = MongoClient("mongodb://localhost:27017")
mongo_db = mongo_connection["lnkd-llm"]

def users_collection():
    return mongo_db["users"]

users_collection().insert_one({
    "api_key": str(ULID()),
    "active": True,
    "user_id": str(ULID()),
    "username": "Customer 1",
    "email": "rahul.works.sde@gmail.com",
    "phone": "9999999999"
})