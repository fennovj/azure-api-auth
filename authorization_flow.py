import requests
import dotenv
 
tenant_id = dotenv.dotenv_values(".env").get("TENANT_ID")

# We need to call the /authorize endpoint first
url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
params = {
    "client_id": "04b07795-8ddb-461a-bbee-02f9e1bf7b46",  # This is the Azure CLI client ID
    "response_type": "code",
    "redirect_uri": "http://localhost:56266",  # This should match your redirect URI in Azure AD
    "scope": "https://management.core.windows.net//.default offline_access openid profile",
    "state": "jXRiAoehKMOLqJvp",  # Random state value to prevent CSRF attacks
    "code_challenge": "lvzdBAI01goIpY44PkMomMAAl8EK8oChracZGusZ3Ys",  # Code challenge for PKCE
    "code_challenge_method": "S256",
    "nonce": "da444824df481e1d7f622b7c9108b113c234de9ce0382d594d074cc845187522",
    "client_info": "1",
    "claims": '{"access_token": {"xms_cc": {"values": ["CP1"]}}}',
    "prompt": "select_account"
}

# I gave up here for now and decided to try the device code flow instead.