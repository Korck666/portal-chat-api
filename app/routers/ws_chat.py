import json
from time import sleep
from fastapi import APIRouter, Depends, WebSocket
from services.authenticator import Authenticator
from services.openai import OpenAI
from services.logger import Logger

logger = Logger()
# import openai
router = APIRouter()
openai = OpenAI()


class WebsocketMessage:
    message: str
    worldId: str
    id: str


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        chunks = []
        messages = []
        # Wait for the client to send a message
        websocket_receive = await websocket.receive_text()

        message_input = json.loads(websocket_receive)
        # Send the message to the ChatGPT model and get a response
        response = openai.chat(
            "gpt-3.5-turbo", "You are a helpful assistant.", message_input.get('message'), stream=True)

        # Iterate over the response and send each message
        for chunk in response:
            # get the message from the response
            # chunks.append(chunk["choices"][0]["delta"])
            message_json = {
                "message": messages[-1],
                "id": message_input.get('id')
            }
            messages.append(chunk["choices"][0]["delta"].get("content", ""))

            await websocket.send_text(json.dumps(message_json))
            sleep(0.1)
