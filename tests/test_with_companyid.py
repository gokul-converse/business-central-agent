# # For this particular company, give me its customers

# from app.business_central.client import BusinessCentralClient

# from app.config.settings import settings


# client = BusinessCentralClient()

# customers = client.get(
#     f"companies({settings.bc_company_id})/customers"
# )

# print("Customers retrieved successfully!")
# print(customers["value"][0])  # Print the first customer in the list


# Give me this specific customer.
from app.business_central.client import BusinessCentralClient
from app.config.settings import settings


client = BusinessCentralClient()

customer_id = "5bbfbe6b-8376-f111-a5be-6045bdfb7c14"

customer = client.get(
    f"companies({settings.bc_company_id})/customers({customer_id})"
)

print("Customer retrieved successfully!")
print(customer)