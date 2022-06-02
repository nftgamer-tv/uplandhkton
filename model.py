from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel,validator




#Pydantic Schema
class UplandUserCreate(BaseModel):
    userId:str
    eosId:str
    username:str
    networth:int
    level:str
    accessToken:str


class UplandUser(UplandUserCreate):
    id:str
    

class UplandPayload(BaseModel):
    type:str
    data:dict
    

class UplandOAuth(BaseModel):
    code:str
    expireAt:str
    
    

class UplandEscrowContainerCreate(BaseModel):
    containerid:int
    description:str
    appId:int
    expirationDate:str
    status:str


class UplandEscrowContainer(UplandEscrowContainerCreate):
    id:str


class EscrowTransaction(BaseModel):
    id:str
    containerId:int
    ownerEosId:str
    transactionId:int

# MongoDB Converter


def createuplandUserModel(doc) -> UplandUser:
    col = UplandUser(
        id=str(doc['_id']),
        userId=doc['userId'],
        eosId=doc['eosId'],
        username=doc['username'],
        networth=doc['networth'],
        level=doc['level'],
        accessToken=doc['accessToken'],
    )
    return col


def createuplandEscrowContainerModel(doc)-> UplandEscrowContainer:
    col = UplandEscrowContainer(
        id=str(doc['_id']),
        containerid=int(doc['containerid']),
        description=doc['description'],
        appId=int(doc['appId']),
        expirationDate=doc['expirationDate'],
        status=doc['status'],
    )
    return col