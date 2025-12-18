# oauth.py
import os
import time
import requests

ACCOUNT_ID = os.getenv("NETSUITE_ACCOUNT_ID")
CLIENT_ID = os.getenv("NETSUITE_CLIENT_ID")
CLIENT_SECRET = os.getenv("NETSUITE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("NETSUITE_REDIRECT_URI")

TOKEN_URL = f"https://{ACCOUNT_ID}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v2/token"

_token_cache = {
    "access_token": None,
    "expires_at": 0,
    "refresh_token": os.getenv("NETSUITE_REFRESH_TOKEN")  # guardado en Render
}

# 🔹 SOLO UNA VEZ (manual)
def exchange_code_for_tokens(auth_code: str):
    response = requests.post(
        TOKEN_URL,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI
        }
    )

    response.raise_for_status()
    return response.json()


# 🔹 USO PRODUCTIVO
def get_netsuite_token():
    now = time.time()

    if _token_cache["access_token"] and now < _token_cache["expires_at"]:
        return _token_cache["access_token"]

    response = requests.post(
        TOKEN_URL,
        auth=(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "refresh_token",
            "refresh_token": _token_cache["refresh_token"]
        }
    )

    response.raise_for_status()
    data = response.json()

    expires_in = int(data.get("expires_in", 3600))

    _token_cache["access_token"] = data["access_token"]
    _token_cache["expires_at"] = now + expires_in - 60

    return _token_cache["access_token"]

