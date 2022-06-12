from schema import *
from datetime import datetime, timedelta
from aioeos import EosAccount, EosTransaction, EosAction
from aioeos import EosJsonRpc



async def mintNFT(authorizeAcc:EosAccount, rpc:EosJsonRpc, data:MintNFTData):
    action = EosAction(account='nftgamecards',name='mintcard',authorization=[authorizeAcc.authorization('active')],data={
            'collection':data.collection,
            'schema':data.nft_schema,
            'mint_to_acct': data.mint_to_acct,
            'realname': data.realname,
            'imghash': data.imghash,
            'template_id': data.template_id,
            'howmany':data.howmany
        })
    block = await rpc.get_head_block()
    transaction = EosTransaction(expiration=datetime.now() + timedelta(minutes=2),
                                 ref_block_num=block['block_num'] & 65535,
                                 ref_block_prefix=block['ref_block_prefix'],
                                 actions=[action])
    try:
        response = await rpc.sign_and_push_transaction(transaction, keys=[authorizeAcc.key])
        return response
    except Exception as e:
        print(str(e))