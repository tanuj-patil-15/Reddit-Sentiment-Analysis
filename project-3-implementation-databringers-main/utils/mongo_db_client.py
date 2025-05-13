import pymongo
from gc import collect
from typing import Collection
import os
from dotenv import load_dotenv
load_dotenv('src/.env')

db_name = "movieData"
client = None
conStr = None



def getMongoDBClient(conStrIn):
    client = pymongo.MongoClient(conStrIn)
    return client

# function to fetch mongo connection string
def getConnectionString():
    connectionString ='mongodb://localhost:27017'

# function to get mongo collection object
def getCollection(db_name, collection_name):
    global client
    global conStr
    if client is  None:
        conStr = getConnectionString()
    if client is  None:
        client = getMongoDBClient(conStr)
    database =client[db_name]
    collection = database[collection_name]
    return collection

# function to close mongo db connection
def close():
    if client is not None:
        client.close()

#  multiple is a required parameter - accepted values - true / false
#  when multiple is true data has to be a iterable object
#  when multiple is false data shouled be a flat a flat object
def insert(data, collection_name, multiple, db_name=db_name):
    collection = getCollection(db_name, collection_name)
    if multiple is True:
        collection.insert_many(data)
    else :    
        collection.insert_one(data)

def update(filter,data, collection_name, dbname=db_name):
    collection = getCollection(db_name, collection_name)
    collection.update_one(filter,{"$set":data},True)

def getData(collection_name, dbname=db_name):
    collection = getCollection(db_name, collection_name)
    return collection.find()