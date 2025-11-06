from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

# path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__).rsplit("/", 1)[0])

KEY = os.getenv("KEY")
HOST = os.getenv("HOST")
MODEL_DEEPSEEK = os.getenv("MODEL_DEEPSEEK")
MODEL_QUEN = os.getenv("MODEL_QUEN")
MODEL_QUEN_EMBEDDINGS = os.getenv("OLLAMA_EMBEDDINGS")


# Constant settings for the application
MAX_TIME_TO_WAIT = 60  # seconds
RETRIES = 3
MAX_TOKENS = 128

# ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST")
