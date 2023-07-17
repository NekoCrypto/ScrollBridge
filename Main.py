from web3 import Web3
from eth_abi import encode
import random
import time

from BridgeAbi import scroll_bridge_abi
from Config import (
    private_key,
    bridge_addres_contract,
    GETH_address_contract,
    SCROLL_RPC,
    GOERLI_RPC
)

web3 = Web3(Web3.HTTPProvider(GOERLI_RPC))
print(f'Connection is: {web3.is_connected}')

address = Web3.to_checksum_address(web3.eth.account.from_key(private_key=private_key).address)

def scroll_bridge():
    # Bridge contract from Goerli -> Scroll
    scroll_bridge_contract = web3.to_checksum_address(bridge_addres_contract)
    bridge_contrat_scroll = web3.eth.contract(scroll_bridge_contract, abi=scroll_bridge_abi)

    GETH = int(web3.to_wei(0.01, 'ether'))

    bridge_transaction = bridge_contrat_scroll.functions.depositETH({
            10000000000000000, # 0.01 GETH
            40000,
    }).build_transaction({
        'nonce': web3.eth.get_transaction_count(address),
        'gas': 20000,
        'gasPrice': web3.eth.gas_price,
        'from': address,
        'value': web3.to_Wei(0.01, 'ether'),
    })

    time.sleep(3)
    print('Start TX')

    sign_transaction = web3.eth.account.sign_transaction(bridge_transaction, private_key)
    send_transaction = web3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    tx = web3.eth.wait_for_transaction_receipt(send_transaction)

    print(f'Bridge Done from Goerli -> Scroll with HASH {tx}')

scroll_bridge()

print('end')
