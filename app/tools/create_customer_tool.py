from agent_framework import tool

from app.models.customer import CustomerCreateRequest
from app.services.customer_service import CustomerService
from typing import Annotated

customer_service = CustomerService()

@tool(name="create_customer", description = "Create a new customer in Business Central.")
def create_customer(display_name: Annotated[str, "Name of the customer to create in Business Central."]):
    request = CustomerCreateRequest(
        display_name=display_name
    )

    customer = customer_service.create_customer(request)

    return {
        "status": "created",
        "customer": customer
    }