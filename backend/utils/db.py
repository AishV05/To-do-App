from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.todo_db
tasks_collection = db.tasks
users_collection = db.users



