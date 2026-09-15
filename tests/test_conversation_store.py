from app.database.database import SessionLocal
from app.database.models import AgentSessionModel
from app.sessions.postgres_conversation_store import (
    PostgresConversationStore,
)


session_id = "conversation_test_001"

# Create the parent agent session first.
with SessionLocal() as db:
    existing_session = db.get(
        AgentSessionModel,
        session_id,
    )

    if existing_session is None:
        db.add(
            AgentSessionModel(
                session_id=session_id,
                service_session_id="test_service_session_001",
            )
        )
        db.commit()


conversation_store = PostgresConversationStore()

conversation_store.save_message(
    session_id=session_id,
    role="user",
    content="My name is Ravi.",
)

conversation_store.save_message(
    session_id=session_id,
    role="assistant",
    content="Nice to meet you, Ravi.",
)

conversation_store.save_message(
    session_id=session_id,
    role="user",
    content="I work as an AI Engineer.",
)

messages = conversation_store.get_messages(
    session_id=session_id,
    limit=10,
)

for message in messages:
    print(message)