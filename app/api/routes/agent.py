'''This is the configuration for Inmemory session management.'''

# from fastapi import APIRouter

# from app.agents.bc_agent import agent
# from app.api.request import ChatRequest

# from app.sessions.session_store import get_or_create_session

# router = APIRouter()


# @router.post("/chat")
# async def chat(request: ChatRequest):

#     session = get_or_create_session(request.session_id)

#     response = await agent.run(request.message,
#                                session=session)

#     return {
#         "session_id": request.session_id,
#         "response": response.text
#     }

'''This is for the configuration for Postgres session management.'''

from fastapi import APIRouter
from app.agents.bc_agent import agent
from app.api.request import ChatRequest
from agent_framework import AgentSession
from app.sessions.postgres_session_store import PostgresSessionStore
from app.sessions.postgres_conversation_store import PostgresConversationStore

session_store = PostgresSessionStore()
conversation_store = PostgresConversationStore()

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):

    # 1. Find existing Foundry service session
    service_session_id = session_store.get_service_session_id(
        request.session_id
    )

    # 2. Reuse existing session or create a new one
    if service_session_id:
        session = AgentSession(
            service_session_id=service_session_id
        )
    else:
        session = agent.create_session()

    # 3. Send user message to the agent
    response = await agent.run(
        request.message,
        session=session
    )

    # print("\n========== CURRENT RESPONSE ==========")         -----> DEBUGGING PURPOSES

    # for index, message in enumerate(response.messages):
    #     print(f"\n--- Message {index + 1} ---")
    #     print("Role:", message.role)
    #     for content_index, content in enumerate(message.contents):
    #         print(f"\nContent {content_index + 1}")
    #         print("Type:", type(content))
    #         print("Data:", vars(content))

    # print("\n========== SESSION DATA ==========")
    # print(session.to_dict())


    # 4. Get the Foundry service session ID
    session_data = session.to_dict()

    service_session_id = session_data.get(
        "service_session_id"
    )

    # 5. Save application session mapping
    if service_session_id:
        session_store.save_session(
            request.session_id,
            service_session_id
        )

        # 6. Save user message in our PostgreSQL memory
        conversation_store.save_message(
            session_id=request.session_id,
            role="user",
            content=request.message
        )

        # 7. Save assistant response in our PostgreSQL memory
        conversation_store.save_message(
            session_id=request.session_id,
            role="assistant",
            content=response.text
        )

        # 8. Return response to frontend
        return {
            "session_id": request.session_id,
            "response": response.text
        }


'''
Final mental model

STM is working, but it is controlled by the Foundry service. Our application currently remembers only the mapping from session_id to service_session_id.

For custom context management, our next step is to create an application-owned conversation message table in PostgreSQL and record each user message and assistant response.
'''


'''Create application owned conversation message table in PostgreSQL and record each user message and assistant response. But currently, the PostgreSQL messages are not being read and injected into the agent prompt. This is currently only storing a copy of the conversation.'''