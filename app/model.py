from datetime import datetime
from typing import Optional,List
from pydantic import BaseModel,validator




#Pydantic Schema
class UplandUser(BaseModel):
    userId:str
    eosId:str
    username:str
    networth:int
    level:str
    accessToken:str
  

class UplandPayload(BaseModel):
    type:str
    data:dict
    

class UplandOAuth(BaseModel):
    code:str
    expireAt:str
    
    

class UplandEscrowContainer(BaseModel):
    containerid:int
    description:str
    appId:int
    expirationDate:str
    status:str


class EscrowTransaction(BaseModel):
    containerId:int
    ownerEosId:str
    transactionId:int
    

class UserDividedStructure(BaseModel):
    eosId:str
    structureId:str

    
class MintNFTData(BaseModel):
    collection:str
    nft_schema:str
    mint_to_acct:str
    realname:str
    imghash:str
    template_id:int
    howmany:int


class UserWaxMapping(BaseModel):
    eosId:str
    waxId:str
    

# MongoDB Converter

def createUserWaxMapping(doc) -> UserWaxMapping:
    col = UserWaxMapping(
        eosId=doc['eosId'],
        waxId=doc['waxId'],
    )
    return col
    

def createuplandUserModel(doc) -> UplandUser:
    col = UplandUser(
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
        containerid=int(doc['containerid']),
        description=doc['description'],
        appId=int(doc['appId']),
        expirationDate=doc['expirationDate'],
        status=doc['status'],
    )
    return col