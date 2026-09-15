"""
"Hey Business Central, I have an access token from Microsoft Entra ID. Can you give me the data from your API?"
"""


import httpx

from app.auth.bc_auth import BcAuth
from app.config.settings import settings


class BusinessCentralClient:
    def __init__(self):
        self.auth = BcAuth()

        self.base_url = (
            f"{settings.bc_base_url}"
            f"/v2.0"
            f"/{settings.bc_environment}"
            f"/api"
            f"/{settings.bc_api_version}"
        )

    def get(self, endpoint: str):
        access_token = self.auth.get_access_token()

        url = f"{self.base_url}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        response = httpx.get(
            url,
            headers=headers,
        )

        response.raise_for_status()   # If BC says 200 - continue, else raise an error.

        return response.json()


    def post(self, endpoint: str, payload: dict):
        access_token = self.auth.get_access_token()

        url = f"{self.base_url}/{endpoint}"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        response = httpx.post(
            url,
            headers=headers,
            json=payload,
        )

        response.raise_for_status()

        return response.json()

    def patch(
    self,
    endpoint: str,
    payload: dict,
    headers: dict | None = None,
):
        access_token = self.auth.get_access_token()

        url = f"{self.base_url}/{endpoint}"

        request_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if headers:
            request_headers.update(headers)

        response = httpx.patch(
            url,
            headers=request_headers,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


    def delete(self, endpoint:str, headers: dict | None = None):
        access_token = self.auth.get_access_token()
        url = f"{self.base_url}/{endpoint}"

        request_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "applcation/json"
        }

        if headers:
            request_headers.update(headers)

        response = httpx.delete(url, headers=request_headers)
        response.raise_for_status()

        if response.status_code == 204:
            return {"status": "deleted",
                    "message": "Customer deleted successfully."}

        return response.json()