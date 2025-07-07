import requests
import dotenv

# Just going to to use these as global variables for simplicity
# The goal is not enterprise code, just a showcase
config = dotenv.dotenv_values(".env")
tenant_id = config.get("TENANT_ID")
client_id = config.get("CLIENT_ID")
client_secret = config.get("CLIENT_SECRET")

resp = requests.post(
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
    headers = { "Content-Type": "application/x-www-form-urlencoded" },
    data = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
)

assert resp.status_code == 200, f"Failed to get access token with message {resp.text}"

resp2 = requests.get(
    "https://graph.microsoft.com/v1.0/groups/",
    headers = {
        "Authorization": f"Bearer {resp.json()['access_token']}"
    }
)

assert resp2.status_code == 200, f"Failed to get users with message {resp2.text}"

print(resp.json())