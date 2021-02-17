import subprocess
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
from eth_account import Account
from bit import wif_to_key
from bit import PrivateKeyTestnet
from constants import *

currency = [BTCTEST, ETH]
coins =[]

def derive_wallets(coin):
    command = f'Desktop/wallet/derive -g --mnemonic="slam visa disorder clinic ticket easy comic toddler they sound smoke galaxy" --coin={coin} --numderive=3 --cols=path,address,privkey,pubkey --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    keys = json.loads(output)
    return keys

eth_wallets=derive_wallets(ETH)
btctest_wallets=derive_wallets(BTCTEST)

coins = {"btc-test":btctest_wallets,"eth": eth_wallets}

coins = json.dumps(coins, indent=2)

print(coins)

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Web3.eth.accounts.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def create_tx(coin, account, recipient, amount):
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
            "nonce": w3.eth.getTransactionCount(account.address),}
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        tx = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()

    elif coin == BTCTEST:
        key = wif_to_key("")
        addresses = [recipient]

        outputs = []

        for address in addresses:
            outputs.append((address, amount, "btc"))
        return print(key.send(outputs))



from web3.middleware import geth_poa_middleware







    




