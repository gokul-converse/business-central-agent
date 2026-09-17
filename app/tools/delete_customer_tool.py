from agent_framework import tool
from app.models.customer import CustomerDeleteRequest
from app.services.customer_service import CustomerService
from app.exceptions.bc_exceptions import BusinessCentralAPIError
from typing import Annotated

customer_service = CustomerService()

@tool(name="delete_customer", description = "Delete an existing customer in the Business central. Use this tool when the user explicitly asks to delete or remove a customer.",
      approval_mode = "always_require")
def delete_customer(display_name: Annotated[str, "Name of the existing customer to delete"]):
    customer_delete_request = CustomerDeleteRequest(
        display_name=display_name
    )

    try:
        result = customer_service.delete_customer(
            customer_delete_request
        )

        return result

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
                "deleting the customer."
            ),
            "error_code": "UnexpectedError",
        }

# Only Approval mode is not enought, Our /chat endpoint must know how to handle the approval request.

"""
Your current flow is:

request.message
      ↓
agent.run()
      ↓
response.text
      ↓
return response

---

With HITL, it becomes:

request.message
      ↓
agent.run()
      ↓
Check pending approval
      ↓
If approval required → return approval details
      ↓
If no approval → return normal response
"""