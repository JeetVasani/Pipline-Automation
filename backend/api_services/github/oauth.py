# for github oauth
import httpx
import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

def exchange_code(code: str):
    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }

    res = httpx.post(url, headers=headers, data=data)
    return res.json()    # contains access_token
