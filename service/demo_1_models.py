import logging
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
import random
from constants.config import (
    KEY,
    HOST,
    MODEL_QUEN,
    MAX_TIME_TO_WAIT,
    RETRIES,
    MAX_TOKENS,
)

logger = logging.getLogger(__name__)

class DemoModel:

    @staticmethod
    def chat(question: str):
        logger.info(f"DemoModel.chat method called with question: {question}")

        if not MODEL_QUEN:
            logger.error("MODEL_QUEN must be set in constants.config")
            raise ValueError("MODEL_QUEN must be set in constants.config")
        if not KEY:
            logger.error("KEY must be set in constants.config")
            raise ValueError("KEY must be set in constants.config")

        seed = random.randint(0, 999999)
        logger.debug(f"Using seed for ChatOpenAI: {seed}")
        logger.debug(f"ChatOpenAI config: model={MODEL_QUEN}, host={HOST}, timeout={MAX_TIME_TO_WAIT}, retries={RETRIES}, max_tokens={MAX_TOKENS}")

        try:
            model = ChatOpenAI(
                model=MODEL_QUEN,
                api_key=SecretStr(KEY),
                base_url=HOST,
                temperature=1.7,  # bigger value means more randomness
                seed=seed,
                timeout=MAX_TIME_TO_WAIT,
                max_retries=RETRIES,
                max_completion_tokens=MAX_TOKENS,
                verbose=True,
                verbosity="medium",
            )

            response = model.invoke(
                f"""
                    Question:
                    - {question}
                    settings (must follow!):
                    - in max 3 lines.
                    - giving replay in raw markdown format.
                    - it should be in json format (json format should be structured and valid).
                    - key will be topic and value will be the reason. (I.E. biological: he has something...)
                    - markdown code should have language information like ```<language> content... ``` (I.E. ```json {{}}```)
                    - it should be consistent int one human language
                """
            )
            logger.info("Successfully received response from ChatOpenAI.")
            return response.content
        except Exception as e:
            logger.error(f"Error during ChatOpenAI invocation: {e}", exc_info=True)
            raise
