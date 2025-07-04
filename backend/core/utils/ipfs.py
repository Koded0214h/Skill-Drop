import requests
import os

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PINATA_BASE_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

def upload_to_ipfs(metadata: dict):
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
    }
    response = requests.post(PINATA_BASE_URL, json={"pinataContent": metadata}, headers=headers)
    
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
    else:
        raise Exception("Failed to upload metadata to IPFS: " + response.text)
