from pydantic import BaseModel, Field


class Customer(BaseModel):
    id: str
    number: str
    name: str
    phone: str | None = None
    email: str | None = None
    city: str | None = None
    country: str | None = None

class CustomerCreateRequest(BaseModel):
    display_name: str = Field(description="Name of the customer to create in Business Central.")

class CustomerUpdateRequest(BaseModel):
    display_name: str = Field(description="Name of the existing customer to update.")
    number: str | None = Field(default=None, description="Customer number used to identify the customer.")
    phone: str | None = Field(default=None, description="New phone number for the customer.")
    email: str | None = Field(default=None, description="New email address for the customer.")
    city: str | None = Field(default=None, description="New city for the customer.")
    country: str | None = Field(default=None, description="New country for the customer.")

class CustomerDeleteRequest(BaseModel):
    display_name: str = Field(description="Name of the existing customer to delete.")