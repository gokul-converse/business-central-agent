from app.services.customer_service import CustomerService


service = CustomerService()

customers = service.search_customers(phone="233445566", name = "Adatum")

print("Search result:")
print(customers)