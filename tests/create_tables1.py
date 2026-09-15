from app.database.database import Base, engine

# Import models so SQLAlchemy registers their tables.
from app.database.models import (
    AgentSessionModel,
    ConversationMessageModel,
)

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")



"""
And the new table:

conversation_messages
-----------------------------
id
session_id
role
content
created_at

will manage:

Our chat ID → Our own conversation messages"""


"""
So:

PostgreSQL
├── agent_sessions
│   └── session_id → service_session_id
│
└── conversation_messages
    └── session_id → user/assistant messages"""