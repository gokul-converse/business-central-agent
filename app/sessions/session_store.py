# in-memory session management:

from app.agents.bc_agent import agent


sessions = {}


def get_or_create_session(session_id: str):

    if session_id not in sessions:
        sessions[session_id] = agent.create_session()

    return sessions[session_id]