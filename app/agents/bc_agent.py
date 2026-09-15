from app.config.settings import client
from agent_framework import Agent
from app.tools.search_customer_tool import search_customers
from app.tools.create_customer_tool import create_customer
from app.tools.update_customer_tool import update_customer
from app.tools.delete_customer_tool import delete_customer

agent = Agent(
    client=client,
    name="Business Central Agent",
    description=(
        "An AI assistant that helps users interact with "
        "Business Central data using available tools."
    ),
     instructions="""
        You are a Business Central assistant.

        Understand the user's request and use the available
        Business Central tools when required.

        Use tool results as the source of truth for Business Central data.
        Do not invent or assume Business Central information.

        If a tool returns no results, clearly inform the user.

        If a tool returns multiple results, present the relevant
        records clearly and ask for clarification when necessary.

        If the user's request is missing information required to
        complete the task, ask the user for clarification.

        Keep responses clear, concise, and useful.
        """,
        tools=[search_customers, create_customer, update_customer, delete_customer]
        )


