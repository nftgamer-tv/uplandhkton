import imp
import os
from urllib import response
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode
import json
import httpx
from typing import List
from datetime import datetime, timedelta
from schema import *
import repositories
import utils


from aioeos import EosAccount, EosTransaction, EosAction
from aioeos import EosJsonRpc


eosName = os.getenv('EOS_NAME')
eosKey = os.getenv('EOS_KEY')
rpcEndPoint = os.getenv('RPC_ENDPOINT')
AppID = os.getenv('AppID')
APPSecrete= os.getenv('APPSecrete')
URL = os.getenv('UPLAND_API')

nft_authorizer = EosAccount(
    name=eosName,
    private_key=eosKey
)

rpc = EosJsonRpc(url=rpcEndPoint)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/upland/webhook', status_code=200)
async def upland_webhook(payload:UplandPayload):
    if payload.type == 'AuthenticationSuccess':
        await storeAppAuthenticatedUser(payload.data)
    # elif payload.type == 'TransactionToEscrowCreated':
    #     saveEscrowTransaction(payload.data)
    #     user_wax = database.get_user_wax_mapping(payload.data['ownerEosId'])
    #     nft =  MintNFTData(collection='uplandrentct',
    #                        nft_schema='apartments',
    #                        mint_to_acct=user_wax.waxId,
    #                        realname='Apartment',
    #                        imghash='QmbKfekKYtDmpeoc19VELq7UGEeJNKQmF1HV6TYSFtmU4o',
    #                        template_id=448297,howmany=2)
    #     res = await mintNFT(nft)
    #     print(res)
    
    
async def storeAppAuthenticatedUser(data):
    auth = 'Bearer ' + data['accessToken']
    headers = {'Authorization': auth}
    with httpx.Client(headers=headers) as client:
        r = client.get(f'{URL}/user/profile')
        if r.status_code == 200:
            repositories.saveUser(r.json())
            

@app.get('/upland/user/{eosId}', status_code=200, response_model=UplandUser)
async def get_user_by_EosID(eosId:str):
    user = repositories.fetchUserByEosID(eosId)
    return user


@app.get('/upland/user/{eosId}/wax/{waxId}', status_code=200, response_model=UplandUser)
async def map_user_wax_address(eosId:str, waxId:str):
    userWax = repositories.saveUserWax(eosId,waxId)
    return userWax

@app.post('/upland/structure/isdivided', status_code=200)
async def check_if_structure_divide(data:UserStructureCreate):
    return repositories.checkIfStructureHasBeenDevided(data.eosId, data.structureId)

@app.post('/upland/structure/divide', status_code=200)
async def divide_structure(data:UserStructureCreate):
    return repositories.devideStructure(data.eosId, data.structureId)

@app.post('/upland/{eosId}/mintnft/{structureId}', status_code=200)
async def mintNft(eosId:str,structureId:str,data:MintNFTData):
    user = repositories.fetchUserByEosID(eosId)
    structure = repositories.fetchUserStructure(eosId,structureId)
    if structure.nftIssued:
        raise NFTIssuedExcaption(f'NFT has already been issued for the structure with id {structureId}.')
    
    response = await utils.mintNFT(nft_authorizer,rpc,data)
    return response