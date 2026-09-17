import asyncio

from app.agents.bc_agent import agent
from agent_framework import AgentSession


async def main():

    # 1. Create a fresh session
    session = agent.create_session()

    # 2. Ask the agent to delete a customer
    response = await agent.run(
        "Delete the customer with customer number C00220",
        session=session,
    )

    print("\n========== FIRST RESPONSE ==========")
    print("Text:", response.text)
    print("Finish reason:", response.finish_reason)

    # 3. Check whether MAF requested approval
    if not response.user_input_requests:
        print("\nNo approval request received.")
        return

    # 4. Get the pending approval request
    approval_request = response.user_input_requests[0]

    print("\n========== APPROVAL REQUEST ==========")
    print("Request ID:", approval_request.id)
    print("Type:", approval_request.type)
    print("Approved:", approval_request.approved)

    # 5. Simulate human approval in console
    user_input = input(
        "\nApprove deletion? Type yes or no: "
    ).strip().lower()

    if user_input == "yes":
        approved = True
    elif user_input == "no":
        approved = False
    else:
        print("Please enter only yes or no.")
        return

    # 6. Convert human decision into MAF approval response
    approval_response = (
        approval_request.to_function_approval_response(approved)
    )

    print("\n========== APPROVAL RESPONSE ==========")
    print(approval_response)

    # 7. Resume the same agent session
    final_response = await agent.run(
        approval_response,
        session=session,
    )

    print("\n========== FINAL RESPONSE ==========")
    print(final_response.text)


if __name__ == "__main__":
    asyncio.run(main())