from urllib.parse import urlencode
from src.variables import OS_BASE_URL, OS_KEY
import requests


def os_api_call(headers, params, offset=0):
    full_url = f"{OS_BASE_URL}{urlencode(params, {"offset": offset})}"
    try:
        response = requests.get(full_url, headers=headers)
        data = response.json()
        return data
    except Exception:
        return False


def os_places_api_call(uprn):
    full_url = f"https://api.os.uk/search/places/v1/uprn?uprn={uprn}&key={OS_KEY}"
    try:
        response = requests.get(full_url)
        data = response.json()
        return data
    except Exception:
        return False