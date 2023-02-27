import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

var_mongo_user= os.getenv('MONGO_USERNAME')
var_mongo_pass= os.getenv('MONGO_PASS')
var_mongodb = os.getenv('MONGO_DATABASE')

conn = MongoClient("mongodb+srv://root:root@cluster0.t2yu0.mongodb.net/?retryWrites=true&w=majority")
mongodatabase = conn[var_mongodb]