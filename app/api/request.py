from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    session_id: str                 # Which conversation does this message belong to