import asyncio

from app.agents.bc_agent import agent
from agent_framework import AgentSession


async def main():

    session = agent.create_session()

    first = await agent.run(
        "My name is Ravi",
        session=session
    )

    print("First response:")
    print(first.text)

    data = session.to_dict()

    print("\nSerialized:")
    print(data)

    restored_session = AgentSession.from_dict(data)

    second = await agent.run(
        "What is my name?",
        session=restored_session
    )

    print("\nSecond response:")
    print(second.text)


asyncio.run(main())