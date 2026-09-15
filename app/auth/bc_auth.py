# bc_auth.py → its job is to obtain a valid Business Central access token from Microsoft Entra ID.

from azure.identity import ClientSecretCredential # this will handle the OAuth 2.0 flow for us, using the client credentials grant type.(SDK)
# "We use Azure Identity's ClientSecretCredential, which internally handles the OAuth 2.0 Client Credentials flow with Microsoft Entra ID to acquire an access token."
from app.config.settings import settings


class BcAuth:
    def __init__(self):
        self.credential = ClientSecretCredential(
            tenant_id=settings.bc_tenant_id,
            client_id=settings.bc_client_id,
            client_secret=settings.bc_client_secret,
        )

    def get_access_token(self) -> str:
        token = self.credential.get_token(
            "https://api.businesscentral.dynamics.com/.default"
        )

        # print(token)

        return token.token