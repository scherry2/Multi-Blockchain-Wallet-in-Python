from constants import *
from dotenv import load_dotenv
import os
load_dotenv()
from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from web3 import Web3
from eth_account import Account

mnemonic=os.getenv("mnemonic")

print(type(mnemonic))

import subprocess
import json


def derive_wallets(mnemonic=mnemonic, coin=BTC, numderive=3):
    command = f'./derive -g --mnemonic="{mnemonic}" --coin={coin} --numderive={numderive} --cols=path,address,privkey,pubkey --format=jsonpretty'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    print(keys)
    return keys


coins={
    'ETH':derive_wallets(coin=ETH),
    'BTCTEST':derive_wallets(coin=BTCTEST)
    
}
print(coins)

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def priv_key_to_account(coin,priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BICTEST:
        return PrivateKeyTestnet(priv_key)


def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    
    
def send_tx(coin, account, to, amount):
    tx = create_tx(coin, account, to, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    elif coin == BTCTEST:
        return NetworkAPI.broadcast_tx_testnet(signed)
account_one=priv_key_to_account(BTCTEST,coins[BTCTEST][0]['privkey'])

print(coins[BTCTEST][0]['privkey'])

account_two=coins[BTCTEST][1]['address']