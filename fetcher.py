import requests
import json

def load_config(chain):
    with open("config.json") as f:
        config = json.load(f)
    return config.get(chain)


def fetch_transactions(address, start_block, end_block, chain, api_key, page=1, offset=100, sort="asc"):
    """
    Fetches transactions for a given address and block range using Etherscan's API.
    """
    config = load_config(chain)  # Ensure the chain is valid
    if not config:
        raise ValueError(f"Chain {chain} is not configured.")
    
    etherscan_url = f"{config['rpc_url']}/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": start_block,
        "endblock": end_block,
        "page": page,
        "offset": offset,
        "sort": sort,
        "apikey": api_key
    }
    
    response = requests.get(etherscan_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching transactions: {response.status_code} {response.text}")
    
    data = response.json()
    if data["status"] != "1" or "result" not in data:
        raise Exception(f"Error in Etherscan API response: {data.get('message', 'Unknown error')}")
    
    return data["result"]

# Example usage
# if __name__ == "__main__":
#     transactions = fetch_transactions(
#         address="0xabc",
#         start_block=0,
#         end_block=99999999,
#         chain="ethereum",
#         api_key="YourApiKeyToken"
#     )
#     print(json.dumps(transactions, indent=2))
