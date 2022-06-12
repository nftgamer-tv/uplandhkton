from urllib import response
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode
import json
import httpx
from typing import List
from model import UserWaxMapping
import database as database
from model import MintNFTData, UplandPayload, UplandUser,UplandOAuth, UserDividedStructure
from model import UplandEscrowContainer
from datetime import datetime, timedelta

## Testnet testing

from aioeos import EosAccount, EosTransaction, EosAction
from aioeos import EosJsonRpc

nft_account = EosAccount(
    name='use your eos',
    private_key='key'
)


rpc = EosJsonRpc(url='https://waxtestnet.greymass.com')



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

URL = 'https://api.sandbox.upland.me/developers-api'

AppID = '78'
APPSecrete='ad740220-0e13-4f59-82c4-8dc8a7c42503'


# @app.post('/webhook', status_code=200)
# async def webhook(request: Request, response: Response):
#     """ Webhook for Upland Hackathon.
#     """
#     content = await request.json()
#     if 'type'  in content:
#         print(content['data'])
#     print(content)


@app.post('/upland/webhook', status_code=200)
async def upland_webhook(payload:UplandPayload):
    if payload.type == 'AuthenticationSuccess':
        await savedAuthenticatedUser(payload.data)
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



@app.get('/upland/user/{eosId}', status_code=200, response_model=UplandUser)
async def get_user_by_EosID(eosId:str):
    user = database.fetch_user_by_EosID(eosId)
    return user

@app.get('/upland/user/{eosId}/wax/{waxId}', status_code=200, response_model=UserWaxMapping)
async def map_user_wax_address(eosId:str, waxId:str):
    userWax = database.save_user_wax(eosId,waxId)
    return userWax


@app.get('/upland/user/{eosId}/wax/', status_code=200, response_model=UserWaxMapping)
async def get_user_wax_address(eosId:str):
    userWax = database.get_user_wax_mapping(eosId)
    return userWax


@app.post('/upland/auth', status_code=200, response_model=UplandOAuth)
async def authenticate():
    with httpx.Client(auth=(AppID, APPSecrete)) as client:
        r = client.post(f'{URL}/auth/otp/init')
        if r.status_code == 201:
            authData = r.json()
            return UplandOAuth(code=authData['code'],expireAt=authData['expireAt'])
        else:
            print(r.status_code)


@app.post('/upland/containers', status_code=200)
async def createContainer(description:str,expirationPeriodHours:int):
    with httpx.Client(auth=(AppID, APPSecrete)) as client:
        r = client.post(f'{URL}/containers', data={'expirationPeriodHours': expirationPeriodHours})
        if r.status_code == 201:
            containerData = r.json()
            containerData['description'] = description
            print(containerData)
            # container = UplandEscrowContainerCreate(description=description,containerid=containerData['id'],appId=containerData['appId'],expirationDate=containerData['expirationDate'],status=containerData['status'])
            database.add_container(containerData)
            return containerData
        else:
            print(r.status_code)
            return f'Server Issue message: {r.text}'
        

@app.get('/upland/containers/{id}', status_code=200)
async def getContainerById(id:str):
    with httpx.Client(auth=(AppID, APPSecrete)) as client:
        r = client.get(f'{URL}/containers/{id}')
        if r.status_code == 200:
            return r.json()
        else:
            print(r.status_code)
            return 'Server Issue'

@app.post('/upland/containers/{id}/refresh', status_code=200)
async def refreshContainer(id:str):
    with httpx.Client(auth=(AppID, APPSecrete)) as client:
        r = client.post(f'{URL}/containers/{id}/refresh-expiration-time')
        if r.status_code == 204:
            return 'Done'
        else:
            print(r.status_code)
            return f'Server Issue: Code {r.status_code}. message: {r.text}'


@app.post('/upland/structure/isdivided', status_code=200)
async def check_if_structure_divide(data:UserDividedStructure):
    return database.check_if_building_is_divided(data.eosId, data.structureId)

@app.post('/upland/structure/divide', status_code=200)
async def divide_structure(data:UserDividedStructure):
    return database.divide_structure(data)
    

@app.get('/upland/containers', status_code=200, response_model=List[UplandEscrowContainer])
async def getContainers():
    containers = database.fetch_containers()
    return containers


# @app.get('/upland/building/{userId}/divide', status_code=200, response_model=List[UplandEscrowContainer])
# async def divideBuilding(userId:str):
#     containers = database.fetch_containers()
#     return containers


@app.post('/upland/mintNFT', status_code=200)
async def mintNft(data:MintNFTData):
    response = await mintNFT(data)
    return response



async def savedAuthenticatedUser(data):
    auth = 'Bearer ' + data['accessToken']
    headers = {'Authorization': auth}
    with httpx.Client(headers=headers) as client:
        r = client.get(f'{URL}/user/profile')
        if r.status_code == 200:
            userData = r.json()
            user = database.add_upland_user(userData)
            print(user)
            
async def storeAppAuthenticatedUser(data):
    auth = 'Bearer ' + data['accessToken']
    headers = {'Authorization': auth}
    with httpx.Client(headers=headers) as client:
        r = client.get(f'{URL}/user/profile')
        if r.status_code == 200:
            userData = r.json()
            user = UplandUser(**userData)
            user = database.add_upland_user(userData)
            print(user)


def saveEscrowTransaction(data):
    doc = database.add_escrowTransaction(data)
    print(doc)
        
        

    