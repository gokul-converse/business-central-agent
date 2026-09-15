from app.business_central.client import BusinessCentralClient
from app.config.settings import settings

from app.models.customer import Customer, CustomerCreateRequest, CustomerUpdateRequest, CustomerDeleteRequest

class CustomerService:

    def __init__(self):
        self.client = BusinessCentralClient()

    @staticmethod
    def _escape_odata_value(value: str) -> str:
        return value.replace("'", "''")


    #The caller can provide any of these search criteria.
    def search_customers(                                       # MAF automatically transformed that into a structured schema: while it is wrapped in the @tool decorator, it is automatically transformed into a structured schema that can be used by an agent to call this function as a tool.
        self,
        name: str | None = None,
        number: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        top: int = 10
    ):
        if not any([name, number, phone, email]):
            raise ValueError(
                "At least one search criterion must be provided."
            )

        filters = []

        if name:
            name = self._escape_odata_value(name)
            filters.append(f"contains(displayName, '{name}')")

        if number:
            number = self._escape_odata_value(number)
            filters.append(f"number eq '{number}'")

        if phone:
            phone = self._escape_odata_value(phone)
            filters.append(f"phoneNumber eq '{phone}'")

        if email:
            email = self._escape_odata_value(email)
            filters.append(f"email eq '{email}'")

        filter_query = " and ".join(filters)

        endpoint = (
            f"companies({settings.bc_company_id})"
            f"/customers?$filter={filter_query}&$top={top}"
        )

        # all_customers = []
        # next_url = endpoint         # Start by calling the first page. (our original BC API URL)

        # while next_url:
        #     response = self.client.get(next_url)

        #     customers = response.get("value", [])
        #     all_customers.extend(customers)

        #     next_url = response.get("@odata.nextLink")


        all_customers = []
        next_url = endpoint    # Start by calling the first page. (our original BC API URL)

        while next_url and len(all_customers) < top:
            response = self.client.get(next_url)

            customers = response.get("value", [])

            remaining = top - len(all_customers)
            all_customers.extend(customers[:remaining])

            next_url = response.get("@odata.nextLink")


            customer_models = [
                    Customer(
                        id=customer["id"],
                        number=customer["number"],
                        name=customer["displayName"],
                        phone=customer.get("phoneNumber"),
                        email=customer.get("email"),
                        city=customer.get("city"),
                        country=customer.get("country"),
                    )
                    for customer in all_customers
                ]

        if not customer_models:
            return {
                "status": "not_found",
                "customers": []
            }

        if len(customer_models) == 1:
            return {
                "status": "found",
                "customers": customer_models
            }

        return {
            "status": "multiple",
            "customers": customer_models
        }

    def create_customer(
        self,
        customer: CustomerCreateRequest
    ):
        payload = {
            "displayName": customer.display_name
        }

        endpoint = (
            f"companies({settings.bc_company_id})"
            f"/customers"
        )

        response = self.client.post(
            endpoint,
            payload
        )

        return Customer(
            id=response["id"],
            number=response["number"],
            name=response["displayName"],
            phone=response.get("phoneNumber"),
            email=response.get("email"),
            city=response.get("city"),
            country=response.get("country"),
        )


    def update_customer(self, customer: CustomerUpdateRequest):
        if not any([
            customer.number,
            customer.phone,
            customer.email,
            customer.city,
            customer.country,
        ]):
            raise ValueError(
                "At least one customer property must be provided for update."
            )

        # Step 1: Find the customer
        search_result = self.search_customers(
            name=customer.display_name,
            number=customer.number,
        )

        if search_result["status"] == "not_found":
            return {
                "status": "not_found",
                "customers": [],
            }
        
        if search_result["status"] == "multiple":
            return {
                "status": "multiple",
                "customers": search_result["customers"],
            }

        matched_customer = search_result["customers"][0]

        # Step 2: Build PATCH payload
        payload = {}

        if customer.phone is not None:
            payload["phoneNumber"] = customer.phone

        if customer.email is not None:
            payload["email"] = customer.email

        if customer.city is not None:
            payload["city"] = customer.city

        if customer.country is not None:
            payload["country"] = customer.country

        # Step 3: Update the customer in Business Central
        endpoint = (
            f"companies({settings.bc_company_id})"
            f"/customers({matched_customer.id})"
        )

        response = self.client.patch(
            endpoint,
            payload,
            headers={
                "If-Match": "*"
            },
        )

        # Step 4: Return the updated customer
        return Customer(
            id=response["id"],
            number=response["number"],
            name=response["displayName"],
            phone=response.get("phoneNumber"),
            email=response.get("email"),
            city=response.get("city"),
            country=response.get("country"),
        )

    def delete_customer(self, customer: CustomerDeleteRequest):
        # Find the customer by display name
        search_result = self.search_customers(name=customer.display_name)

        if search_result["status"] == "not_found":
            return {
                "status" : "not_found",
                "message" : f"No customer found with display name '{customer.display_name}'."
            }

        if search_result["status"] == "multiple":
            return{
                "status": "Multiple",
                "customers": search_result["customers"],
                "message": f"Multiple customer found, Please provide more specific customer name or number to delete."
            }

        matched_customer = search_result["customers"][0]

        endpoint = (
            f"companies({settings.bc_company_id})"
            f"/customers({matched_customer.id})"
        )

        self.client.delete(
            endpoint,
            headers={"If-Match": "*"}
            )

        return {
            "status": "deleted",
            "message": (
                f"Customer '{matched_customer.name}' "
                f"with number '{matched_customer.number}' "
                f"was deleted successfully."
                ),
            "customer": matched_customer,
    }
        

        