# models/ChatOutput.py
from pydantic import BaseModel


class ChatOutput(BaseModel):
    response: str
