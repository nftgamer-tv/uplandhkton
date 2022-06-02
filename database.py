from enum import unique
import os
import model
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from datetime import timezone

url_value = os.getenv('DB_URL', 'mongodb+srv://nftgamertv:7NupwZc2jFvUOJtm@nftgamertv.dspl8.mongodb.net/nftgUpland?retryWrites=true&w=majority')
db_name_value = os.getenv('DB_TABLE', 'nftgUpland')
client = MongoClient(url_value)
database = client[db_name_value] 

uplandusers = database.uplandusers
containers = database.containers
escrowTransactions = database.escrowTransactions


def add_upland_user(data:model.UplandUser):
    doc = fetch_user_by_Id(data.userId)
    if doc is None:
        doc = uplandusers.insert_one(data.dict())
        return model.createuplandUserModel(doc)
    else:
        uplandusers.update_one({'_id':doc['_id']}, {'$set': data.dict()})
        doc = fetch_user_by_Id(data.userId)
        return model.createuplandUserModel(doc)
 

def fetch_user_by_Id(userId):
    doc =  uplandusers.find_one({'userId': userId})
    return doc


def fetch_upland_players():
    docs = []
    for doc in uplandusers.find():
        docs.append(model.createuplandUserModel(doc))
    return docs



def add_container(data:model.UplandEscrowContainerCreate):
    doc = fetch_container_by_id(data.containerid)
    if doc is None:
        doc = containers.insert_one(data.dict())
        return model.createuplandEscrowContainerModel(doc)
    else:
        containers.update_one({'_id':doc['_id']}, {'$set': data.dict()})
        doc = fetch_container_by_id(data.containerid)
        return model.createuplandEscrowContainerModel(doc)
    
    
def fetch_container_by_id(containerId):
    doc =  containers.find_one({'containerid': containerId})
    return doc


def fetch_containers():
    docs = []
    for doc in containers.find():
        docs.append(model.createuplandEscrowContainerModel(doc))
    return docs


def add_escrowTransaction(data):
    print(data['transactionId'])
    doc = fetch_escrowTransaction_byId(data['transactionId'])
    if doc is None:
        doc = escrowTransactions.insert_one(data)
    else:
        escrowTransactions.update_one({'_id':doc['_id']}, {'$set': data})
        doc = fetch_escrowTransaction_byId(data.containerid)
    return doc


def fetch_escrowTransaction_byId(transactionID):
    doc =  escrowTransactions.find_one({'transactionId': transactionID})
    return doc