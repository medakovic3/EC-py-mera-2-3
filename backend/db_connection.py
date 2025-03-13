from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "EnergyCalculator"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def get_db():
    return db

# Test database connection
# collections = db.list_collection_names()
# print("Collections in database:", collections)