from app.business_central.client import BusinessCentralClient
from app.config.settings import settings


client = BusinessCentralClient()

endpoint = (
    f"companies({settings.bc_company_id})"
    f"/customers"
)

payload = {
    "displayName": "AI Test Customer 001"
}

response = client.post(
    endpoint,
    payload
)

print(response)