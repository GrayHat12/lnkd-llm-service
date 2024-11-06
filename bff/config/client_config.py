from common_constants.service_constants import DATABASE_NAME, USER_DB, REQUEST_LOG, LNKD_REQUESTS
from .app_config import load_app_config, parse_arguments
import os
import pymongo

parse_arguments()
load_app_config()

# If DB_URI not in environment, throws a KeyError
mongo_connection = pymongo.MongoClient(os.environ['DB_URI'])
mongo_db = mongo_connection[DATABASE_NAME]


def user_db():
    return mongo_db[USER_DB]

def request_log_db():
    return mongo_db[REQUEST_LOG]

def lnkd_request_db():
    return mongo_db[LNKD_REQUESTS]