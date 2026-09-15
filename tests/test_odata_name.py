# from app.business_central.client import BusinessCentralClient
# from app.config.settings import settings


# client = BusinessCentralClient()

# endpoint = (
#     f"companies({settings.bc_company_id})"
#     f"/customers?$filter=displayName eq 'Adatum Corp'"
# )

# customers = client.get(endpoint)

# print("Filtered customers:")
# print(customers)


# # DYNAMIC FILTERING - Exact matching
# from app.business_central.client import BusinessCentralClient
# from app.config.settings import settings


# client = BusinessCentralClient()

# customer_name = input("Enter customer name: ")

# endpoint = (
#     f"companies({settings.bc_company_id})"
#     f"/customers?$filter=displayName eq '{customer_name}'"
# )

# customers = client.get(endpoint)

# print("Filtered customers:")
# print(customers)


# DYNAMIC FILTERING - Partial matching
from app.business_central.client import BusinessCentralClient
from app.config.settings import settings


client = BusinessCentralClient()

customer_name = input("Enter customer name: ")

endpoint = (
    f"companies({settings.bc_company_id})"
    f"/customers?$filter=contains(displayName, '{customer_name}')"
)

customers = client.get(endpoint)

print("Filtered customers:")
print(customers)