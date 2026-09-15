from app.services.customer_service import CustomerService
from app.models.customer import CustomerCreateRequest


service = CustomerService()

request = CustomerCreateRequest(
    display_name="AI Test Customer 002"
)

customer = service.create_customer(request)

print(customer)