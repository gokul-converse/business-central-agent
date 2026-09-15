from app.tools.search_customer_tool import search_customers


result = search_customers(
    name="Adatum",
    phone="233445566"
)

print("Tool result:")
print(result)

print("\nTool type:")
print(type(search_customers))

print("\nTool name:")
print(search_customers.name)

print("\nTool description:")
print(search_customers.description)

print("\nTool parameters:")
print(search_customers.parameters())