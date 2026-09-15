from app.auth.bc_auth import BcAuth


auth = BcAuth()

access_token = auth.get_access_token()

print("Authentication successful!")
print(f"Access token received: {'Yes' if access_token else 'No'}")

"""Our application used its Entra application credentials, 
and the Azure Identity SDK handled the OAuth 2.0 Client Credentials flow to obtain an access token from Microsoft Entra ID."""