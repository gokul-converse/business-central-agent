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



# # app/services/bc_client.py

# import httpx

# from app.auth.bc_auth import BcAuth
# from app.config.settings import settings
# from app.exceptions.bc_exceptions import BusinessCentralAPIError

# class BusinessCentralClient:
#     def __init__(self):
#         self.auth = BcAuth()            # For getting token from Microsoft Entra ID.

#         self.base_url = (               # Builds the common Business Central API URL.
#             f"{settings.bc_base_url}"
#             f"/v2.0"
#             f"/{settings.bc_environment}"
#             f"/api"
#             f"/{settings.bc_api_version}"
#         )

#     def _request(
#         self,
#         method: str,
#         endpoint: str,
#         *,
#         payload: dict | None = None,
#         headers: dict | None = None,
#     ):
#         url = f"{self.base_url}/{endpoint}"

#         # First attempt: use normal cached/valid token
#         access_token = self.auth.get_access_token()

#         request_headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Accept": "application/json",
#         }

#         if payload is not None:
#             request_headers["Content-Type"] = "application/json"

#         if headers:
#             request_headers.update(headers)

#         response = httpx.request(
#             method=method,
#             url=url,
#             headers=request_headers,
#             json=payload,
#         )

#         # If token is valid, return the response normally
#         if response.status_code != 401:
#             response.raise_for_status()
#             return self._parse_response(response)

#         # 401 received:
#         # Token may have expired during the request.
#         print("Received 401. Requesting a fresh access token...")

#         fresh_access_token = self.auth.get_access_token(
#             force_refresh=True
#         )

#         retry_headers = {
#             "Authorization": f"Bearer {fresh_access_token}",
#             "Accept": "application/json",
#         }

#         if payload is not None:
#             retry_headers["Content-Type"] = "application/json"

#         if headers:
#             retry_headers.update(headers)

#         # Retry exactly once
#         retry_response = httpx.request(
#             method=method,
#             url=url,
#             headers=retry_headers,
#             json=payload,
#         )

#         retry_response.raise_for_status()

#         return self._parse_response(retry_response)

#     def _parse_response(self, response: httpx.Response):
#         if response.status_code == 204:
#             return {
#                 "status": "deleted",
#                 "message": "Customer deleted successfully.",
#             }

#         return response.json()

#     def get(self, endpoint: str):
#         return self._request(
#             method="GET",
#             endpoint=endpoint,
#         )

#     def post(self, endpoint: str, payload: dict):
#         return self._request(
#             method="POST",
#             endpoint=endpoint,
#             payload=payload,
#         )

#     def patch(
#         self,
#         endpoint: str,
#         payload: dict,
#         headers: dict | None = None,
#     ):
#         return self._request(
#             method="PATCH",
#             endpoint=endpoint,
#             payload=payload,
#             headers=headers,
#         )

#     def delete(
#         self,
#         endpoint: str,
#         headers: dict | None = None,
#     ):
#         return self._request(
#             method="DELETE",
#             endpoint=endpoint,
#             headers=headers,
#         )



import httpx

from app.auth.bc_auth import BcAuth
from app.config.settings import settings
from app.exceptions.bc_exceptions import BusinessCentralAPIError


class BusinessCentralClient:
    def __init__(self):
        self.auth = BcAuth()                        # # For getting token from Microsoft Entra ID.

        self.base_url = (                           # # Builds the common Business Central API URL.
            f"{settings.bc_base_url}"
            f"/v2.0"
            f"/{settings.bc_environment}"
            f"/api"
            f"/{settings.bc_api_version}"
        )

    def _build_headers(                             # prepares request headers 
        self,
        access_token: str,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> dict:
        """
        Build the HTTP headers required by Business Central.
        """

        request_headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        if payload is not None:                     # If we send data using POST or PATCH, then: Content-Type is also added
            request_headers["Content-Type"] = "application/json"

        if headers:
            request_headers.update(headers)

        return request_headers                      # The method returns the final headers dictionary

    def _extract_error_details(                     # reads the raw BC error
        self,
        response: httpx.Response,
    ) -> tuple[str, str | None]:
        """
        Extract a useful error message and error code
        from the Business Central response.
        """

        default_message = (
            "Business Central returned an unexpected error."
        )

        try:
            error_data = response.json()

            error_details = error_data.get("error", {})

            error_message = error_details.get(
                "message",
                default_message,
            )

            error_code = error_details.get("code")

            return error_message, error_code

        except ValueError:
            # Response was not valid JSON.
            return response.text or default_message, None

    def _raise_business_central_error(              # creates our custom exception (This method receives the failed response.)
        self,
        response: httpx.Response,                   # This method receives the failed response.
    ) -> None:
        """
        Convert an HTTP error response into our custom exception.
        """

        error_message, error_code = self._extract_error_details(
            response
        )

        raise BusinessCentralAPIError(              # The raw error becomes our custom error:
            message=error_message,
            status_code=response.status_code,
            error_code=error_code,
        )

    def _parse_response(                            # handles successful responses
        self,
        response: httpx.Response,
    ):
        """
        Convert a successful HTTP response into Python data.
        """

        if response.status_code == 204:             # For DELETE, Business Central may return: 204 No Content. There is no JSON body in a 204 response. In that case, we return a custom success message.
            return {
                "status": "success",
                "message": "Operation completed successfully.",
            }

        try:
            return response.json()

        except ValueError as exc:
            raise BusinessCentralAPIError(
                message="Business Central returned an invalid response.",
                status_code=response.status_code,
                error_code="InvalidResponse",
            ) from exc

    def _send_request(                              # actually calls Business Central
        self,
        method: str,
        url: str,
        access_token: str,
        *,
        payload: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        """
        Send one HTTP request to Business Central.
        """

        request_headers = self._build_headers(
            access_token=access_token,
            payload=payload,
            headers=headers,
        )

        try:
            return httpx.request(
                method=method,
                url=url,
                headers=request_headers,
                json=payload,
                timeout=30.0,
            )

        except httpx.TimeoutException as exc:
            raise BusinessCentralAPIError(
                message=(
                    "Business Central took too long to respond. "
                    "Please try again."
                ),
                error_code="RequestTimeout",
            ) from exc

        except httpx.RequestError as exc:
            raise BusinessCentralAPIError(
                message=(
                    "Unable to connect to Business Central. "
                    "Please try again later."
                ),
                error_code="ConnectionError",
            ) from exc

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: dict | None = None,
        headers: dict | None = None,
    ):
        """
        Common request method used by GET, POST, PATCH and DELETE.
        """

        url = f"{self.base_url}/{endpoint}"

        # -------------------------------------------------
        # 1. Get the normal cached/valid access token
        # -------------------------------------------------
        access_token = self.auth.get_access_token()

        # -------------------------------------------------
        # 2. Send the first request
        # -------------------------------------------------
        response = self._send_request(
            method=method,
            url=url,
            access_token=access_token,
            payload=payload,
            headers=headers,
        )

        # -------------------------------------------------
        # 3. If the token expired, refresh and retry once
        # -------------------------------------------------
        if response.status_code == 401:
            print(
                "Received 401 from Business Central. "
                "Refreshing access token and retrying once..."
            )

            fresh_access_token = self.auth.get_access_token(
                force_refresh=True
            )

            response = self._send_request(
                method=method,
                url=url,
                access_token=fresh_access_token,
                payload=payload,
                headers=headers,
            )

        # -------------------------------------------------
        # 4. Handle all non-success HTTP responses
        # -------------------------------------------------
        if response.is_error:
            self._raise_business_central_error(response)

        # -------------------------------------------------
        # 5. Parse and return successful response
        # -------------------------------------------------
        return self._parse_response(response)

    def get(self, endpoint: str):
        return self._request(
            method="GET",
            endpoint=endpoint,
        )

    def post(
        self,
        endpoint: str,
        payload: dict,
    ):
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