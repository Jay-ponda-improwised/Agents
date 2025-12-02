import logging
import random
from typing import cast
from langchain_openai import ChatOpenAI
from service.model_service import get_model_service
from config.enums import ModelName

logger = logging.getLogger(__name__)

class DemoModel:

    @staticmethod
    def chat(question: str):
        logger.info(f"DemoModel.chat method called with question: {question}")

        model_service = get_model_service()
        seed = random.randint(0, 999999)
        logger.debug(f"Using seed for ChatOpenAI: {seed}")
        
        try:
            model_instance = model_service.get_model(ModelName.OPENAI_CHAT, seed=seed)
            if not model_instance:
                raise RuntimeError("Failed to get model from ModelService")

            model = cast(ChatOpenAI, model_instance)

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
