import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None


def init_db(app):
    global _client, _db
    uri = os.getenv("MONGODB_URI")
    _client = MongoClient(uri)
    _db = _client["tasks_db"]
    app.config["DB"] = _db


def get_collection(name):
    return _db[name]
