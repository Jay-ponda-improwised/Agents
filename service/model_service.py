import logging
from typing import Any
from pydantic import SecretStr
from config.models import MODELS_CONFIG
from config.enums import ModelName
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

class ModelService:
    _instance = None
    _singletons = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        logger.info("Loading singleton models from config...")
        for model_name, model_data in MODELS_CONFIG.items():
            if model_data.get("singleton", True):
                try:
                    model_instance = self._create_model_instance(model_data)
                    if model_instance:
                        self._singletons[model_name] = model_instance
                except Exception as e:
                    logger.error(f"Error creating instance for model '{model_name}': {e}", exc_info=True)
        logger.info(f"Successfully loaded {len(self._singletons)} singleton models.")

    def _create_model_instance(self, model_data: dict, extra_config: dict = {}):
        provider = model_data.get("provider")
        config = model_data.get("config", {}).copy()
        if extra_config:
            config.update(extra_config)

        if provider == "ollama":
            logger.debug(f"Initializing OllamaEmbeddings with config: {config}")
            return OllamaEmbeddings(**config)
        elif provider == "huggingface":
            logger.debug(f"Initializing HuggingFaceEmbeddings with config: {config}")
            return HuggingFaceEmbeddings(**config)
        elif provider == "openai":
            logger.debug(f"Initializing ChatOpenAI with config: {config}")
            if 'api_key' in config and config['api_key'] is not None:
                config['api_key'] = SecretStr(config['api_key'])
            
            if 'seed' in config:
                if 'model_kwargs' not in config:
                    config['model_kwargs'] = {}
                config['model_kwargs']['seed'] = config.pop('seed')

            return ChatOpenAI(**config)
        else:
            logger.warning(f"Unknown model provider: {provider}")
            return None

    def get_model(self, model_name: ModelName, **kwargs) -> Any:
        if model_name in self._singletons:
            if kwargs:
                logger.warning(f"Configuration overrides are not supported for singleton model '{model_name.value}'. Ignoring kwargs.")
            return self._singletons.get(model_name)

        model_data = MODELS_CONFIG.get(model_name)
        if not model_data:
            logger.error(f"Model '{model_name.value}' not found in MODELS_CONFIG.")
            return None
            
        return self._create_model_instance(model_data, extra_config=kwargs)

# Singleton instance
model_service = ModelService()

def get_model_service():
    return model_service
