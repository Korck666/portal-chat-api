# app/engine/ai_service_type.py
from enum import Enum


class AIServiceType(Enum):
    # Text Embedding Model: These AI services provide capabilities to convert
    # text into numerical vectors that can be processed by machine learning algorithms.
    TEXT_EMBEDDING = "text_embedding"

    # Text Reasoning Model: These AI services provide capabilities to understand
    # and reason about the text, often used for tasks like question answering or
    # text classification.
    TEXT_REASONING = "text_reasoning"

    # Text Summarizer Model: These AI services provide capabilities to generate
    # a concise summary of a larger text.
    TEXT_SUMMARIZER = "text_summarizer"

    # Image to Text Model: These AI services provide capabilities to understand
    # the content of an image and describe it in text, often used for tasks like
    # image captioning.
    IMAGE_TO_TEXT = "image_to_text"

    # Text to Image Model: These AI services provide capabilities to generate an
    # image based on a text description, often used for tasks like text-based
    # image synthesis.
    TEXT_TO_IMAGE = "text_to_image"

    # Text to Audio Model: These AI services provide capabilities to convert
    # text into spoken words, often used for tasks like text-to-speech synthesis.
    TEXT_TO_AUDIO = "text_to_audio"

    # Audio to Text Model: These AI services provide capabilities to convert spoken
    # words into written text, often used for tasks like speech recognition.
    AUDIO_TO_TEXT = "audio_to_text"

    # Prompt Edit Model: These AI services provide capabilities to modify and
    # improve a given text prompt.
    PROMPT_EDIT = "prompt_edit"
