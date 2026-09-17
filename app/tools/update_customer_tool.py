from agent_framework import tool
from app.exceptions.bc_exceptions import BusinessCentralAPIError
from app.models.customer import CustomerUpdateRequest
from app.services.customer_service import CustomerService
from typing import Annotated

customer_service = CustomerService()

@tool(name="update_customer", 
    description = 
    ("Update an existing customer in Business Central."
    "The customer is identified by display name. "
    "Use this tool to update the customer's phone number, "
    "email address, city, or country."))

def update_customer(
    display_name: Annotated[str, "Name of the existing customer to update."],
    number: Annotated[str | None, "Customer number used to identify the customer."] = None,
    phone: Annotated[str | None, "New phone number for the customer."] = None,
    email: Annotated[str | None, "New email address for the customer."] = None,
    city: Annotated[str | None, "New city for the customer."] = None,
    country: Annotated[str | None, "New country for the customer."] = None,):

    request = CustomerUpdateRequest(
        display_name=display_name,
        number=number,
        phone=phone,
        email=email,
        city=city,
        country=country,
    )

    try:
        result = customer_service.update_customer(request)

        return result

    except BusinessCentralAPIError as exc:
        return {
            "status": "error",
            "message": exc.message,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
        }

    except ValueError as exc:
        return {
            "status": "invalid_input",
            "message": str(exc),
        }

    except Exception:
        return {
            "status": "error",
            "message": (
                "An unexpected error occurred while "
                "updating the customer."
            ),
            "error_code": "UnexpectedError",
        }