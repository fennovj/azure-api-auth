import requests
import dotenv
import time

tenant_id = dotenv.dotenv_values(".env").get("TENANT_ID")
subscription_id = dotenv.dotenv_values(".env").get("SUBSCRIPTION_ID")

client_id = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # This is the Azure CLI client ID

r_devicecode = requests.post(
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/devicecode",
    headers = { "Content-Type": "application/x-www-form-urlencoded" },
    data = {
        "client_id": client_id,
        "scope": "https://management.core.windows.net//.default offline_access openid profile"
    }
)

assert r_devicecode.status_code == 200, f"Failed to get device code with message {r_devicecode.text}"

print(r_devicecode.json()['message'])

# Now we need to poll the /token endpoint until we get a valid access token
while True:
    r_token = requests.post(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        headers = { "Content-Type": "application/x-www-form-urlencoded" },
        data = {
            "client_id": client_id,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": r_devicecode.json()['device_code'],
            "scope": "https://management.core.windows.net//.default offline_access openid profile"
        }
    )
    
    if r_token.status_code == 200:
        print("Access token obtained successfully!")
        break
    elif r_token.status_code == 400 and "authorization_pending" in r_token.text:
        print("Waiting for user to authorize...")
        time.sleep(r_devicecode.json()['interval'])
    else:
        break

assert r_token.status_code == 200, f"Failed to get access token with message {r_token.text}"

# This r_token has an access token, refresh token and id token. I dont really care about the 3rd one
# Try ARM api first

r_arm = requests.get(
    f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Storage/storageAccounts?api-version=2024-01-01",
    headers = {
        "Authorization": f"Bearer {r_token.json()['access_token']}"
    }
)

assert r_arm.status_code == 200, f"Failed to get subscriptions with message {r_arm.text}"


# Now use refresh token to get a graph api token

r_graph_token = requests.post(
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
    headers = { "Content-Type": "application/x-www-form-urlencoded" },
    data = {
        "client_id": client_id,
        "grant_type": "refresh_token",
        "refresh_token": r_token.json()['refresh_token'],
        "scope": "https://graph.microsoft.com/.default"
    }
)

assert r_graph_token.status_code == 200, f"Failed to get graph token with message {r_graph_token.text}"

r_graph = requests.get(
    "https://graph.microsoft.com/v1.0/groups/",
    headers = {
        "Authorization": f"Bearer {r_graph_token.json()['access_token']}"
    }
)

assert r_graph.status_code == 200, f"Failed to get groups with message {r_graph.text}"
