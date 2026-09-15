from agent_framework import tool
from app.services.customer_service import CustomerService

from typing import Annotated

customer_service = CustomerService()

@tool(name="search_customers",                                                              # MAF wraps that function and turns it into something that can be supplied to an agent as a tool.
      description=("Search Business Central customers using name, customer number, "
        "phone number, or email address. Returns matching customer records "
        "up to the specified limit."))   
                                    
def search_customers(           
    name: Annotated[
        str | None,
        "Customer name or partial customer name to search for."
    ] = None,

    number: Annotated[
        str | None,
        "Business Central customer number."
    ] = None,

    phone: Annotated[
        str | None,
        "Customer phone number."
    ] = None,

    email: Annotated[
        str | None,
        "Customer email address."
    ] = None,

    top: Annotated[
        int,
        "Maximum number of customers to return."
    ] = 10,
):
    """
    Search Business Central customers using name, customer number,
    phone number, or email address.
    """

    return customer_service.search_customers(
        name=name,
        number=number,
        phone=phone,
        email=email,
        top=top,
    )