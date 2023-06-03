# models/ChatInput.py
from pydantic import BaseModel


class ChatInput(BaseModel):
    message: str
