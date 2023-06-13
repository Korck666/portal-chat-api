# routers/chat.py
from fastapi import APIRouter, Depends
from pydantic import config
from services.auth import Authenticator
from utils.config import Config
from models.chat_input import ChatInput
from models.chat_output import ChatOutput
from services.openai import OpenAI

router = APIRouter()
chat_model = OpenAI()
config = Config()
auth = Authenticator("api_key")
# TODO: Add config for chat prompts and responses with langchain
chat_prep = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."""


@router.post("/chat", response_model=ChatOutput, dependencies=[Depends(auth.auth_header_dependency)])
def chat_endpoint(chat_input: ChatInput):
    # we may do some preprocessing here
    # Return the response
    return ChatOutput(response=chat_model.chat(config.CHAT_MODEL, chat_prep, chat_input.message))
