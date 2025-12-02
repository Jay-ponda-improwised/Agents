import os
from dotenv import load_dotenv
from config.enums import ModelName, MODEL_QUEN_EMBEDDINGS, MODEL_QUEN

load_dotenv()

# path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__).rsplit("/", 1)[0])

KEY = os.getenv("KEY")
HOST = os.getenv("HOST")
MODEL_DEEPSEEK = os.getenv("MODEL_DEEPSEEK")


# Constant settings for the application
MAX_TIME_TO_WAIT = 60  # seconds
RETRIES = 3
MAX_TOKENS = 128

# ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST")


MODELS_CONFIG = {
    ModelName.OLLAMA_EMBEDDINGS: {
        "provider": "ollama",
        "singleton": True,
        "config": {
            "model": MODEL_QUEN_EMBEDDINGS,
            "base_url": OLLAMA_HOST
        }
    },
    ModelName.HUGGINGFACE_EMBEDDINGS: {
        "provider": "huggingface",
        "singleton": True,
        "config": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
            "cache_folder": ROOT_DIR + "/.cache",
            "show_progress": True,
            "model_kwargs": {"device": "cpu"},
            "encode_kwargs": {"normalize_embeddings": True},
        }
    },
    ModelName.OPENAI_CHAT: {
        "provider": "openai",
        "singleton": True,
        "config": {
            "model": MODEL_QUEN,
            "api_key": KEY,
            "base_url": HOST,
            "temperature": 1.7,
            "timeout": MAX_TIME_TO_WAIT,
            "max_retries": RETRIES,
            "max_completion_tokens": MAX_TOKENS,
            "verbose": True,
            "verbosity": "medium",
        }
    }
}