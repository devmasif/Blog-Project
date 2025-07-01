from pymongo import MongoClient

client = MongoClient("mongodb+srv://user:abcdefgh123@cluster0.hnx7xe8.mongodb.net/")

db = client["blog_db"]
users_collection = db["users"]
posts_collection = db["posts"]
comments_collection = db["comments"]
likes_collection = db["likes"]


