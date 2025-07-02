import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()  

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGO_URI)
assert DB_NAME is not None, "DB_NAME not set in .env"
db = client[DB_NAME]


users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]
likes_collection = db["likes"]