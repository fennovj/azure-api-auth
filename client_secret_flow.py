import requests
import dotenv

# Just going to to use these as global variables for simplicity
# The goal is not enterprise code, just a showcase
config = dotenv.dotenv_values(".env")
tenant_id = config.get("TENANT_ID")
client_id = config.get("CLIENT_ID")
client_secret = config.get("CLIENT_SECRET")
subscription_id = config.get("SUBSCRIPTION_ID")

r_token = requests.post(
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
    headers = { "Content-Type": "application/x-www-form-urlencoded" },
    data = {
        "client_id": client_id,
        "scope": "https://management.core.windows.net/.default",
        #"scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
)

assert r_token.status_code == 200, f"Failed to get access token with message {r_token.text}"

r_arm = requests.get(
    f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Storage/storageAccounts?api-version=2024-01-01",
    headers = {
        "Authorization": f"Bearer {r_token.json()['access_token']}"
    }
)

assert r_arm.status_code == 200, f"Failed to get subscriptions with message {r_arm.text}"

r_graph_token = requests.post(
    f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
    headers = { "Content-Type": "application/x-www-form-urlencoded" },
    data = {
        "client_id": client_id,
        #"scope": "https://management.core.windows.net/.default",
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
)

assert r_graph_token.status_code == 200, f"Failed to get access token with message {r_graph_token.text}"


r_graph = requests.get(
    "https://graph.microsoft.com/v1.0/groups/",
    headers = {
        "Authorization": f"Bearer {r_graph_token.json()['access_token']}"
    }
)

assert r_graph.status_code == 200, f"Failed to get users with message {r_graph.text}"
