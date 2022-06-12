from enum import unique
import os
import model as model
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from datetime import timezone

url_value = os.getenv('DB_URL', 'mongodb://localhost:27017')
db_name_value = os.getenv('DB_TABLE', 'nftgUpland')

client = MongoClient(url_value)
database = client[db_name_value] 

uplandusers = database.uplandusers
containers = database.containers
escrowTransactions = database.escrowTransactions
userdividedstructure = database.userdividedstructure
userwaxmapping = database.userwaxmapping



#  saveUser = UplandUserCreate(userId=userData['id'],eosId=userData['eosId'],accessToken=data['accessToken'],username=userData['username'],networth=userData['networth'],level=userData['level'])

def add_upland_user(data):
    if uplandusers.count_documents({'userId': data['id']}, limit = 1) == 0:
        doc = uplandusers.insert_one(data)
        return doc
    else:
        doc = fetch_user_by_Id(data['id'])
        count = uplandusers.update_one({'_id':doc['_id']}, {'$set': data})
        return count
 

def fetch_user_by_Id(userId):
    doc =  uplandusers.find_one({'userId': userId})
    return doc


def fetch_user_by_EosID(eosId):
    doc =  uplandusers.find_one({'eosId': eosId})
    if doc is not None:
        return model.createuplandUserModel(doc)
    else:
        return None


def fetch_upland_players():
    docs = []
    for doc in uplandusers.find():
        docs.append(model.createuplandUserModel(doc))
    return docs



def add_container(data):
    doc = fetch_container_by_id(data['id'])
    if doc is None:
        doc = containers.insert_one(data)
        return doc
    else:
        containers.update_one({'_id':doc['_id']}, {'$set': data})
        doc = fetch_container_by_id(data['id'])
        return doc
    
    
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


def check_if_building_is_divided(eosid,structureId):
    if userdividedstructure.count_documents({'eosId': eosid, 'structureId':structureId}, limit = 1) != 0:
        return True
    return False
    # doc = userdividedstructure.find_one({'eosId': eosid, 'structureId':structureId})
    # if doc is None:
    #     return True
    # else:
    #     return False


def divide_structure(data:model.UserDividedStructure):
    # doc = userdividedstructure.find_one({'eosId': data.eosId, 'structureId':data.structureId})
    # if doc is None:
    #     doc = userdividedstructure.insert_one(data.dict())
    #     return True
    if not check_if_building_is_divided(data.eosId,data.structureId):
        userdividedstructure.insert_one(data.dict())
        return True
    else:
        return False


def save_user_wax(eosId:str,waxId:str):
    if userwaxmapping.count_documents({'eosId': eosId, 'waxId':waxId}, limit = 1) == 0:
        doc = userwaxmapping.insert_one({'eosId': eosId, 'waxId':waxId})
        return model.createUserWaxMapping(doc)
    else:
        doc = userwaxmapping.find_one({'eosId': eosId, 'waxId':waxId})
        return model.createUserWaxMapping(doc)
    
def get_user_wax_mapping(eosId:str):
    if userwaxmapping.count_documents({'eosId': eosId}, limit = 1) != 0:
        doc = userwaxmapping.find_one({'eosId': eosId})
        return model.createUserWaxMapping(doc)
