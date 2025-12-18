import os
import time
import requests
import base64

NETSUITE_ACCOUNT_ID = os.getenv("NETSUITE_ACCOUNT_ID")
NETSUITE_CLIENT_ID = os.getenv("NETSUITE_CLIENT_ID")
NETSUITE_CLIENT_SECRET = os.getenv("NETSUITE_CLIENT_SECRET")
NETSUITE_REDIRECT_URI = os.getenv("NETSUITE_REDIRECT_URI")

TOKEN_URL = (
    f"https://{NETSUITE_ACCOUNT_ID}.suitetalk.api.netsuite.com"
    "/services/rest/auth/oauth2/v2/token"
)

_token_cache = {
    "access_token": None,
    "expires_at": 0
}

def get_netsuite_token(auth_code: str) -> str:
    if not all([
        NETSUITE_ACCOUNT_ID,
        NETSUITE_CLIENT_ID,
        NETSUITE_CLIENT_SECRET,
        NETSUITE_REDIRECT_URI
    ]):
        raise Exception("❌ Variables de entorno NetSuite incompletas")

    now = time.time()

    if _token_cache["access_token"] and now < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    auth_str = f"{NETSUITE_CLIENT_ID}:{NETSUITE_CLIENT_SECRET}"
    auth_base64 = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": NETSUITE_REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(
            f"❌ OAuth NetSuite error\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text}"
        )

    token_data = response.json()

    expires_in = int(token_data.get("expires_in", 3600))

    _token_cache["access_token"] = token_data["access_token"]
    _token_cache["expires_at"] = now + expires_in - 60

    return _token_cache["access_token"]

