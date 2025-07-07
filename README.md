# azure-api-auth

Personal development project: reverse engineer azure rest api authentication

The goal: using a simple http library like curl or requests, reverse engineer the following:

- `az login`
- `az account get-access-token --scope xxx`
- Make sure we can call the graph api: e.g. <https://graph.microsoft.com/v1.0/groups/>
- Optionally: see if we can get it working with databricks. The most interesting to me:
  - OAuth User to Machine per User
  - OAuth Machine to Machine

If possible, I will get try to get it working both for client_id+client_secret, as well as personal (interactive browser) login.

## Research

### Client secret flow

I started with this document: <https://learn.microsoft.com/en-us/rest/api/azure/>. This mentioned there are two grants: "Authorization code grant" and "Client credentials grant". It seems the second is quite easy, and forwards to <https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-client-creds-grant-flow#get-a-token>

Obtaining a token was doable, but calling the graph api errored with `"Authorization_RequestDenied","message":"Insufficient privileges to complete the operation."`. This is the code in `client_secret_flow.py`.

I decided to try the interactive flow next since I know for sure that I have privileges to make this api call (using `az rest`)