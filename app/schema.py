
from pydantic_mongo import ObjectIdField
from bson.objectid import ObjectId
from typing import Optional,List
from pydantic import BaseModel,validator
from pydantic_mongo import AbstractRepository


#Pydantic Schema
class UplandUser(BaseModel):
    id: ObjectIdField = None
    userId:str
    eosId:str
    username:str
    networth:int
    level:str
    accessToken:str
    waxId:Optional[str] = None
    
    class Config:
        json_encoders = {ObjectId: str}
        

class UserStructureCreate(BaseModel):
    eosId:str
    structureId:str


class UserStructure(UserStructureCreate):
    id: ObjectIdField = None
    eosId:str
    structureId:str
    nftIssued:Optional[bool] = False
    
    class Config:
        json_encoders = {ObjectId: str}


class MintNFTData(BaseModel):
    collection:str
    nft_schema:str
    mint_to_acct:str
    realname:str
    imghash:str
    template_id:int
    howmany:int
    
class UplandPayload(BaseModel):
    type:str
    data:dict
    

class UplandOAuth(BaseModel):
    code:str
    expireAt:str
    
    
    
# pydantic_mongo
class UplandUserRepository(AbstractRepository[UplandUser]):
    class Meta:
        collection_name = 'uplandusers'
        
class UserStructureRepository(AbstractRepository[UserStructure]):
    class Meta:
        collection_name = 'userstructuresmapping'



# Others
class UserNotFoundException(Exception):
    pass


class UserStructureNotFoundException(Exception):
    pass


class NFTIssuedExcaption(Exception):
    pass