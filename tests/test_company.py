from app.business_central.client import BusinessCentralClient


client = BusinessCentralClient()

companies = client.get("companies")

print("Business Central API call successful!")
print(companies)