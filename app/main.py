from fastapi import FastAPI, Depends
from pydantic import BaseModel
import os
import openai

set_key = lambda s: os.getenv(s) if os.getenv(s) is not None else ""

# Initialize OpenAI and Pinecone
openai.api_key = set_key("OPENAI_API_KEY")

# Create FastAPI instance
app = FastAPI()

class ChatInput(BaseModel):
    message: str

class ChatOutput(BaseModel):
    response: str

@app.post("/chat", response_model=ChatOutput)
def chat_endpoint(chat_input: ChatInput):
    # Call OpenAI API
    openai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chat_input.message},
        ]
    )
<<<<<<< HEAD
    response_message = openai_response["choices"][0]["message"]["content"] # type: ignore
=======
    response_message = openai_response.choices[0].message # type: ignore
>>>>>>> 737b5d25ff2dbf608f5deb131ce30aada649313b
    # Return the response
    return ChatOutput(response=response_message)
