import asyncio

from app.agents.bc_agent import agent


async def main():

    response = await agent.run(
        "Find the customer Wizi Tech"
    )

    print([
    x for x in dir(agent)
    if not x.startswith("_")
])

    print("\n========== AGENT DICTIONARY ==========")

    print(agent.__dict__)

    print("\n========== CONFIGURED TOOLS ==========")

    tools = agent.default_options["tools"]

    print("Tools type:")
    print(type(tools))

    print("\nNumber of tools:")
    print(len(tools))

    for i, tool in enumerate(tools):

        print(f"\n===== TOOL {i} =====")

        print("Type:")
        print(type(tool))

        print("\nName:")
        print(tool.name)

        print("\nDescription:")
        print(tool.description)

        print("\nParameters:")
        print(tool.parameters())

    print("\n========== RESPONSE TYPE ==========")
    print(type(response))

    print("\n========== RESPONSE ==========")
    print(response.text)

    print("\n========== RESPONSE ATTRIBUTES ==========")
    print([
        x for x in dir(response)
        if not x.startswith("_")
    ])

    print("\n========== MESSAGES TYPE ==========")
    print(type(response.messages))

    print("\n========== MESSAGE DETAILS ==========")

    for i, message in enumerate(response.messages):

        print(f"\n===== MESSAGE {i} | ROLE: {message.role} =====")

        print("\nMessage Type:")
        print(type(message))

        print("\nMessage Attributes:")
        print([
            x for x in dir(message)
            if not x.startswith("_")
        ])

        print("\nMessage Dictionary:")
        print(message.__dict__)

        print("\n----- CONTENT DETAILS -----")

        for j, content in enumerate(message.contents):

            print(f"\n--- CONTENT {j} ---")

            print("Type:")
            print(type(content))

            print("\nAttributes:")
            print([
                x for x in dir(content)
                if not x.startswith("_")
            ])

            # print("\nDictionary:")
            # print(content.__dict__)


if __name__ == "__main__":
    asyncio.run(main())