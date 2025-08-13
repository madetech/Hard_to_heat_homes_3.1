from src.variables import EPC_BASE_URL, EPC_TOKEN
import requests

def epc_api_call(headers, params):

    full_url = f'{EPC_BASE_URL}{params}'

    try:
        response = requests.get(full_url, headers=headers)
        data = response.json()
        return data
    except Exception:
        return False
    
def epc_api_call_address(params):
    headers = {"Accept": "application/json", "Authorization": f"Basic {EPC_TOKEN}"}
    try:
        response = requests.get(EPC_BASE_URL, params=params, headers=headers)
        data = response.json()
        return data
    except Exception:
        return False