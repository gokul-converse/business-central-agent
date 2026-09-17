from agent_framework import tool

from app.exceptions.bc_exceptions import BusinessCentralAPIError
from app.models.customer import CustomerCreateRequest
from app.services.customer_service import CustomerService
from typing import Annotated

customer_service = CustomerService()

@tool(name="create_customer", description = "Create a new customer in Business Central.")
def create_customer(display_name: Annotated[str, "Name of the customer to create in Business Central."]):
    request = CustomerCreateRequest(
        display_name=display_name
    )

    try:
        customer = customer_service.create_customer(request)

        return {
            "status": "created",
            "message": (
                f"Customer '{display_name}' "
                "was created successfully."
            ),
            "customer": customer.model_dump(),
        }

    except BusinessCentralAPIError as exc:
        return {
            "status": "error",
            "message": exc.message,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
        }

    except Exception:
        return {
            "status": "error",
            "message": (
                "An unexpected error occurred while "
                "creating the customer."
            ),
            "error_code": "UnexpectedError",
        }