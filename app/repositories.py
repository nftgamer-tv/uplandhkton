import os
from pymongo import MongoClient
from schema import *


url_value = os.getenv('DB_URL', 'mongodb://localhost:27017')
db_name_value = os.getenv('DB_TABLE', 'nftgUpland')

client = MongoClient(url_value)
database = client[db_name_value]


upland_User_Repository = UplandUserRepository(database=database)
User_Structure_Repository = UserStructureRepository(database=database)
        

def saveUser(data):
    user = UplandUser(**data)
    result = upland_User_Repository.save(user)


def saveUserWax(esoId,WaxId):
    result = upland_User_Repository.find_one_by({'eosId':esoId})
    if result:
        result.waxId = WaxId
        upland_User_Repository.save(result)
        return result
    else:
        raise UserNotFoundException(f'User with eosId: "{esoId}" not found.')
    
    
def fetchUserByEosID(esoId):
    result = upland_User_Repository.find_one_by({'eosId':esoId})
    if result:
        return result
    else:
        raise UserNotFoundException(f'User with eosId: "{esoId}" not found.')


def fetchUserByUplandUserID(userId):
    result = upland_User_Repository.find_one_by({'userId':userId})
    if result:
        return result
    else:
        raise UserNotFoundException(f'User with userId: "{userId}" not found.')
    

def checkIfStructureHasBeenDevided(eosid,structureId):
    result = User_Structure_Repository.find_one_by({'eosId': eosid, 'structureId':structureId})
    if result:
        return True
    else:
        return False


def devideStructure(eosid,structureId):
    structure = UserStructure(eosId=eosid,structureId=structureId)
    result = User_Structure_Repository.save(structure)
    if result:
        return True
    else:
        return False
    

def fetchUserStructure(eosid,structureId):
    result = User_Structure_Repository.find_one_by({'eosId': eosid, 'structureId':structureId})
    if result:
        return result
    else:
        message = f'Structure for user with eosId: "{eosid}" and structureId: "{structureId}" does not exits on the system. Make sure you have request for the sturcture to be devided.'
        raise UserStructureNotFoundException(message)
    


