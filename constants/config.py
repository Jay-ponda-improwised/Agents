from dotenv import load_dotenv  # type: ignore
import os

load_dotenv()

KEY = os.getenv("KEY")
HOST = os.getenv("HOST")
MODEL_DEEPSEEK = os.getenv("MODEL_DEEPSEEK")
MODEL_QUEN = os.getenv("MODEL_QUEN")
MODEL_QUEN_EMBEDDINGS = os.getenv("HG_TOKEN")


# Constant settings for the application
MAX_TIME_TO_WAIT = 60  # seconds
RETRIES = 3
MAX_TOKENS = 128
