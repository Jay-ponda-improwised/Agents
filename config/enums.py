import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

MODEL_QUEN = os.getenv("MODEL_QUEN", "gpt-3.5-turbo")
MODEL_QUEN_EMBEDDINGS = os.getenv("OLLAMA_EMBEDDINGS", "mxbai-embed-large")


class ModelName(str, Enum):
    OLLAMA_EMBEDDINGS = MODEL_QUEN_EMBEDDINGS
    HUGGINGFACE_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"
    OPENAI_CHAT = MODEL_QUEN
    TRANSFORMERS_SUMMARIZATION = "document-question-answering"
    HUGGINGFACE_API_QUESTION_ANSWERING = "huggingface-api-question-answering"
