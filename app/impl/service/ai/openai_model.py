# app/impl/service/ai/openai_model.py
from app.engine.ai_model import AIModel
import openai


class OpenAIModel(AIModel):
    def __init__(self, model_name):
        self.model_name = model_name

    def query(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message['content'] # type: ignore
