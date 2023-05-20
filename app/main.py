from fastapi import FastAPI, Depends
from pydantic import BaseModel
import os
import openai
import pinecone

# Initialize OpenAI and Pinecone
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))

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
        ],
    )
    response_message = openai_response['choices'][0]['message']['content']

    # Return the response
    return ChatOutput(response=response_message)
