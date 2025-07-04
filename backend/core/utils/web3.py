import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_KEY = os.getenv("PUBLIC_KEY")
RPC_URL = os.getenv("AMOY_RPC")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Load ABI file (relative to this file's directory)
abi_path = os.path.join(os.path.dirname(__file__), "../abi.json")
with open(abi_path, "r") as abi_file:
    abi = json.load(abi_file)

# Connect to Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
assert web3.is_connected(), "Web3 not connected"

# Contract instance
contract = web3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

def mint_badge(recipient_address, token_uri):
    try:
        nonce = web3.eth.get_transaction_count(PUBLIC_KEY)

        txn = contract.functions.mintBadge(
            Web3.to_checksum_address(recipient_address),
            token_uri
        ).build_transaction({
            "from": PUBLIC_KEY,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": web3.to_wei("30", "gwei"),
        })

        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "status": "success",
            "tx_hash": tx_hash.hex(),
            "blockNumber": receipt.blockNumber,
            "recipient": recipient_address
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

