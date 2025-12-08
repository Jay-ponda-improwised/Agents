import logging
from typing import Optional, TypeVar, Generic, Dict, Any
from pydantic import SecretStr
import re
from config.models import MODELS_CONFIG
from config.enums import ModelName
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ModelContainer(Generic[T]):
    """
    A container class to hold a model instance along with its configuration.
    Instantiation is handled by __new__ to adhere to specific design constraints.
    """

    model: T
    config: Dict[str, Any]
    is_singleton: bool

    def __new__(
        cls, model: T, config: Dict[str, Any], is_singleton: bool
    ) -> "ModelContainer[T]":
        """
        Creates and initializes a new ModelContainer instance.

        Args:
            model: The model object instance.
            config: The configuration dictionary used to create the model.
            is_singleton: A boolean indicating if the model is a singleton.

        Returns:
            A new instance of ModelContainer populated with the provided data.
        """
        instance = super().__new__(cls)
        instance.model = model
        instance.config = config
        instance.is_singleton = is_singleton
        return instance


_ollama_embeddings_singleton: Optional[ModelContainer[OllamaEmbeddings]] = None


def init_ollamaEmbeddings(
    force_new: bool = False, **kwargs
) -> ModelContainer[OllamaEmbeddings]:
    """
    Initializes and returns a ModelContainer for an OllamaEmbeddings instance.

    If the model is configured as a singleton, this function will return the
    existing container instance unless `force_new=True` is passed or configuration
    overrides are provided via kwargs.

    Args:
        force_new: If True, a new instance will be created and will replace the
                   existing singleton instance.
        **kwargs: Configuration overrides for the model. Providing kwargs will
                  result in a new instance that is not saved as a singleton.

    Returns:
        A ModelContainer holding the instance of OllamaEmbeddings.
    """
    global _ollama_embeddings_singleton
    model_name = ModelName.OLLAMA_EMBEDDINGS
    model_data = MODELS_CONFIG[model_name]
    is_singleton = model_data.get("singleton", False)

    # Return singleton if it exists and no overrides are requested
    if is_singleton and not force_new and not kwargs and _ollama_embeddings_singleton:
        return _ollama_embeddings_singleton

    config = model_data.get("config", {}).copy()
    config.update(kwargs)

    logger.debug(f"Initializing OllamaEmbeddings with config: {config}")
    instance = OllamaEmbeddings(**config)

    container = ModelContainer(model=instance, config=config, is_singleton=is_singleton)

    # Store as singleton if it's a singleton and this is the first creation
    # or a forced refresh without temporary overrides.
    if is_singleton and not kwargs:
        _ollama_embeddings_singleton = container

    return container


_huggingface_embeddings_singleton: Optional[ModelContainer[HuggingFaceEmbeddings]] = (
    None
)


def init_huggingFaceEmbeddings(
    force_new: bool = False, **kwargs
) -> ModelContainer[HuggingFaceEmbeddings]:
    """
    Initializes and returns a ModelContainer for a HuggingFaceEmbeddings instance.

    If the model is configured as a singleton, this function will return the
    existing container instance unless `force_new=True` is passed or configuration
    overrides are provided via kwargs.

    Args:
        force_new: If True, a new instance will be created and will replace the
                   existing singleton instance.
        **kwargs: Configuration overrides for the model. Providing kwargs will
                  result in a new instance that is not saved as a singleton.

    Returns:
        A ModelContainer holding the instance of HuggingFaceEmbeddings.
    """
    global _huggingface_embeddings_singleton
    model_name = ModelName.HUGGINGFACE_EMBEDDINGS
    model_data = MODELS_CONFIG[model_name]
    is_singleton = model_data.get("singleton", False)

    if (
        is_singleton
        and not force_new
        and not kwargs
        and _huggingface_embeddings_singleton
    ):
        return _huggingface_embeddings_singleton

    config = model_data.get("config", {}).copy()
    config.update(kwargs)

    logger.debug(f"Initializing HuggingFaceEmbeddings with config: {config}")
    instance = HuggingFaceEmbeddings(**config)

    container = ModelContainer(model=instance, config=config, is_singleton=is_singleton)

    if is_singleton and not kwargs:
        _huggingface_embeddings_singleton = container

    return container


_openai_chat_singleton: Optional[ModelContainer[ChatOpenAI]] = None


def init_openAIChat(force_new: bool = False, **kwargs) -> ModelContainer[ChatOpenAI]:
    """
    Initializes and returns a ModelContainer for a ChatOpenAI instance.

    If the model is configured as a singleton, this function will return the
    existing container instance unless `force_new=True` is passed or configuration
    overrides are provided via kwargs.

    Args:
        force_new: If True, a new instance will be created and will replace the
                   existing singleton instance.
        **kwargs: Configuration overrides for the model. Providing kwargs will
                  result in a new instance that is not saved as a singleton.

    Returns:
        A ModelContainer holding the instance of ChatOpenAI.
    """
    global _openai_chat_singleton
    model_name = ModelName.OPENAI_CHAT
    model_data = MODELS_CONFIG[model_name]
    is_singleton = model_data.get("singleton", False)

    if is_singleton and not force_new and not kwargs and _openai_chat_singleton:
        return _openai_chat_singleton

    config = model_data.get("config", {}).copy()
    config.update(kwargs)

    # Handle special case for api_key to wrap it in SecretStr
    if "api_key" in config and config["api_key"] is not None:
        config["api_key"] = SecretStr(config["api_key"])

    # Handle special case for 'seed' to place it in 'model_kwargs'
    if "seed" in config:
        if "model_kwargs" not in config:
            config["model_kwargs"] = {}
        config["model_kwargs"]["seed"] = config.pop("seed")

    logger.debug(f"Initializing ChatOpenAI with config: {config}")
    instance = ChatOpenAI(**config)

    container = ModelContainer(model=instance, config=config, is_singleton=is_singleton)

    if is_singleton and not kwargs:
        _openai_chat_singleton = container

    return container

def convert_prompt(template: str) -> str:
    modified_template = re.sub("[ \n\t\r]+", "⁂", template).strip()
    for line in modified_template.split("⁂"):
        new_line = line.strip()
        if new_line == "" or new_line == "---":
            continue
        modified_template += f" {new_line}⁂"

    return "non readable prompt: ⁂ for new line or separator," +modified_template