from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from base64 import b64encode
import json
import httpx
from typing import List
import database
from model import UplandPayload, UplandUser,UplandUserCreate,UplandOAuth
from model import UplandEscrowContainer, UplandEscrowContainerCreate



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

URL = 'https://api.sandbox.upland.me/developers-api'
AppID = '97'
APPSecrete='7a2c14aa-c346-480a-9226-1ad5e4a4ecba'


@app.post('/webhook', status_code=200)
async def webhook(request: Request, response: Response):
    """ Webhook for Upland Hackathon.
    """
    content = await request.json()
    if 'type'  in content:
        print(content['data'])
    print(content)


@app.post('/upland/webhook', status_code=200)
async def upland_webhook(payload:UplandPayload):
    if payload.type == 'AuthenticationSuccess':
        await savedAuthenticatedUser(payload.data)
    elif payload.type == 'TransactionToEscrowCreated':
        saveEscrowTransaction(payload.data)


@app.get('/upland/players', status_code=200, response_model=List[UplandUser])
async def upland_players():
    players = database.fetch_upland_players()
    return players


@app.post('/upland/auth', status_code=200, response_model=UplandOAuth)
async def authenticate():
    with httpx.Client(auth=(AppID, APPSecrete)) as client:
        r = client.post(f'{URL}/auth/otp/init')
        if r.status_code == 201:
            authData = r.json()
            return UplandOAuth(code=authData['code'],expireAt=authData['expireAt'])
        else:
            print(r.status_code)


@app.post('/upland/containers', status_code=200, response_model=UplandEscrowContainer)
async def createContainer(description:str):
    with httpx.Client(auth=(AppID, APPSecrete)) as client:
        r = client.post(f'{URL}/containers', data={'expirationPeriodHours': 2})
        if r.status_code == 201:
            containerData = r.json()
            container = UplandEscrowContainerCreate(description=description,containerid=containerData['id'],appId=containerData['appId'],expirationDate=containerData['expirationDate'],status=containerData['status'])
            savedcontainer = database.add_container(container)
            return savedcontainer
        else:
            print(r.status_code)
            return 'Server Issue'
        

@app.get('/upland/containers/{id}', status_code=200)
async def createContainer(id:str):
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


@app.get('/upland/containers', status_code=200, response_model=List[UplandEscrowContainer])
async def getContainers():
    containers = database.fetch_containers()
    return containers


@app.get('/upland/building/{userId}/divide', status_code=200, response_model=List[UplandEscrowContainer])
async def divideBuilding(userId:str):
    containers = database.fetch_containers()
    return containers



async def savedAuthenticatedUser(data):
    auth = 'Bearer ' + data['accessToken']
    headers = {'Authorization': auth}
    with httpx.Client(headers=headers) as client:
        r = client.get(f'{URL}/user/profile')
        if r.status_code == 200:
            userData = r.json()
            saveUser = UplandUserCreate(userId=userData['id'],eosId=userData['eosId'],accessToken=data['accessToken'],username=userData['username'],networth=userData['networth'],level=userData['level'])
            user = database.add_upland_user(saveUser)
            print(user)

def saveEscrowTransaction(data):
    doc = database.add_escrowTransaction(data)
    print(doc)
        
        
