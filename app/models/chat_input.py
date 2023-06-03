# models/chat_input.py
from pydantic import BaseModel


class ChatInput(BaseModel):
    message: str
