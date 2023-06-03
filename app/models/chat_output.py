# models/chat_output.py
from pydantic import BaseModel


class ChatOutput(BaseModel):
    response: str
