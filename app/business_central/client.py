"""
"Hey Business Central, I have an access token from Microsoft Entra ID. Can you give me the data from your API?"
"""


# import httpx

# from app.auth.bc_auth import BcAuth
# from app.config.settings import settings


# class BusinessCentralClient:
#     def __init__(self):
#         self.auth = BcAuth()

#         self.base_url = (
#             f"{settings.bc_base_url}"
#             f"/v2.0"
#             f"/{settings.bc_environment}"
#             f"/api"
#             f"/{settings.bc_api_version}"
#         )

#     def get(self, endpoint: str):
#         access_token = self.auth.get_access_token()

#         url = f"{self.base_url}/{endpoint}"

#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Accept": "application/json",
#         }

#         response = httpx.get(
#             url,
#             headers=headers,
#         )

#         response.raise_for_status()   # If BC says 200 - continue, else raise an error.

#         return response.json()


#     def post(self, endpoint: str, payload: dict):
#         access_token = self.auth.get_access_token()

#         url = f"{self.base_url}/{endpoint}"

#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#         }

#         response = httpx.post(
#             url,
#             headers=headers,
#             json=payload,
#         )

#         response.raise_for_status()

#         return response.json()

#     def patch(
#     self,
#     endpoint: str,
#     payload: dict,
#     headers: dict | None = None,
# ):
#         access_token = self.auth.get_access_token()

#         url = f"{self.base_url}/{endpoint}"

#         request_headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#         }

#         if headers:
#             request_headers.update(headers)

#         response = httpx.patch(
#             url,
#             headers=request_headers,
#             json=payload,
#         )

#         response.raise_for_status()

#         return response.json()


#     def delete(self, endpoint:str, headers: dict | None = None):
#         access_token = self.auth.get_access_token()
#         url = f"{self.base_url}/{endpoint}"

#         request_headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Accept": "application/json"
#         }

#         if headers:
#             request_headers.update(headers)

#         response = httpx.delete(url, headers=request_headers)
#         response.raise_for_status()

#         if response.status_code == 204:
#             return {"status": "deleted",
#                     "message": "Customer deleted successfully."}

#         return response.json()



# app/services/bc_client.py

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

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: dict | None = None,
        headers: dict | None = None,
    ):
        url = f"{self.base_url}/{endpoint}"

        # First attempt: use normal cached/valid token
        access_token = self.auth.get_access_token()

        request_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        if payload is not None:
            request_headers["Content-Type"] = "application/json"

        if headers:
            request_headers.update(headers)

        response = httpx.request(
            method=method,
            url=url,
            headers=request_headers,
            json=payload,
        )

        # If token is valid, return the response normally
        if response.status_code != 401:
            response.raise_for_status()
            return self._parse_response(response)

        # 401 received:
        # Token may have expired during the request.
        print("Received 401. Requesting a fresh access token...")

        fresh_access_token = self.auth.get_access_token(
            force_refresh=True
        )

        retry_headers = {
            "Authorization": f"Bearer {fresh_access_token}",
            "Accept": "application/json",
        }

        if payload is not None:
            retry_headers["Content-Type"] = "application/json"

        if headers:
            retry_headers.update(headers)

        # Retry exactly once
        retry_response = httpx.request(
            method=method,
            url=url,
            headers=retry_headers,
            json=payload,
        )

        retry_response.raise_for_status()

        return self._parse_response(retry_response)

    def _parse_response(self, response: httpx.Response):
        if response.status_code == 204:
            return {
                "status": "deleted",
                "message": "Customer deleted successfully.",
            }

        return response.json()

    def get(self, endpoint: str):
        return self._request(
            method="GET",
            endpoint=endpoint,
        )

    def post(self, endpoint: str, payload: dict):
        return self._request(
            method="POST",
            endpoint=endpoint,
            payload=payload,
        )

    def patch(
        self,
        endpoint: str,
        payload: dict,
        headers: dict | None = None,
    ):
        return self._request(
            method="PATCH",
            endpoint=endpoint,
            payload=payload,
            headers=headers,
        )

    def delete(
        self,
        endpoint: str,
        headers: dict | None = None,
    ):
        return self._request(
            method="DELETE",
            endpoint=endpoint,
            headers=headers,
        )