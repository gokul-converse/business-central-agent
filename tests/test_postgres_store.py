from app.sessions.postgres_session_store import PostgresSessionStore


store = PostgresSessionStore()

store.save_session(
    session_id="test_chat_001",
    service_session_id="resp_test_123"
)

print("Session saved.")

service_id = store.get_service_session_id(
    "test_chat_001"
)

print("Retrieved service session ID:")
print(service_id)