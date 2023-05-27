# app/engine/document_type.py
from enum import Enum

class DocumentType(Enum):
    #This is the most basic type of document, which contains only text.
    #   It is often used for storing unstructured data. Example: .txt
    TEXT = "text"

    #This type of document may contains text, audio and images (embedded or referenced).
    #   It is often used for storing structured data. 
    #   Examples include .ppt, .html, .json, .docx, .pdf, .xml and .json
    RICH = "rich"

    #This type of document contains audio.
    #   Examples include .mp3 and .wav
    AUDIO = "audio"

    #This type of document contains text, audio and image. 
    #   Examples include .mp4 and .mov
    VIDEO = "video"

