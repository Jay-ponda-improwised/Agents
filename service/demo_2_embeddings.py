import logging
from constants.config import OLLAMA_HOST, MODEL_QUEN_EMBEDDINGS, ROOT_DIR
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class DemoEmbeddingsService:

    string = """
                {
                    "biological": "Parrots have specialized vocal organs called syrinx that allow them to mimic sounds and human speech.",
                    "social": "They use talking as a form of social bonding and communication within their flock or with humans.",
                    "intelligence": "Parrots are highly intelligent birds that can learn and repeat words to interact with their environment.",
                    "territorial": "Vocal mimicry helps them establish territory and communicate with other birds in the wild.",
                    "entertainment": "Pet parrots often talk to entertain themselves and gain attention from their human companions."
                }
            """.replace(
        r"[ \n\t\r]+", " "
    ).strip()

    documents = [
        "Parrots have specialized vocal organs called syrinx that allow them to mimic sounds and human speech.",
        "They use talking as a form of social bonding and communication within their flock or with humans.",
        "Parrots are highly intelligent birds that can learn and repeat words to interact with their environment.",
        "Vocal mimicry helps them establish territory and communicate with other birds in the wild.",
        "Pet parrots often talk to entertain themselves and gain attention from their human companions.",
    ]

    # Initialize Ollama embeddings
    @property
    def ollama_embeddings(self) -> OllamaEmbeddings:
        logger.info("Accessing ollama_embeddings property.")
        if not MODEL_QUEN_EMBEDDINGS:
            logger.error("MODEL_QUEN_EMBEDDINGS must be set in constants.config")
            raise ValueError("MODEL_QUEN_EMBEDDINGS must be set in constants.config")
        if not ROOT_DIR:
            logger.error("ROOT_DIR must be set in constants.config")
            raise ValueError("ROOT_DIR must be set in constants.config")

        logger.debug(f"Initializing OllamaEmbeddings with model={MODEL_QUEN_EMBEDDINGS}, base_url={OLLAMA_HOST}")
        return OllamaEmbeddings(  # type: ignore[reportGeneralTypeIssues]
            model=MODEL_QUEN_EMBEDDINGS,
            base_url=OLLAMA_HOST,
        )

    @property
    def huggingface_embeddings(self) -> HuggingFaceEmbeddings:
        logger.info("Accessing huggingface_embeddings property.")
        logger.debug(f"Initializing HuggingFaceEmbeddings with model_name='sentence-transformers/all-MiniLM-L6-v2', cache_folder={ROOT_DIR + '/.cache'}")
        return HuggingFaceEmbeddings(  # type: ignore[reportGeneralTypeIssues]
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=ROOT_DIR + "/.cache",
            show_progress=True,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    def convertToEmbeddings(self, text: str):
        logger.info(f"convertToEmbeddings method called with text: {text[:50]}...") # Log first 50 chars
        try:
            # Test the embeddings
            query_result = self.ollama_embeddings.embed_query(text)  # type: ignore[reportGeneralTypeIssues]
            logger.debug(f"Embedding dimension: {len(query_result)}")
            logger.info("convertToEmbeddings completed successfully.")
            return query_result
        except Exception as e:
            logger.error(f"Error in convertToEmbeddings: {e}", exc_info=True)
            raise

    def getEmbeddingsFromDocuments(self, documents: list[str] = documents):
        logger.info(f"getEmbeddingsFromDocuments method called with {len(documents)} documents.")
        try:
            # For multiple documents
            doc_embeddings = self.ollama_embeddings.embed_documents(documents)  # type: ignore[reportGeneralTypeIssues]
            logger.info("getEmbeddingsFromDocuments completed successfully.")
            return doc_embeddings
        except Exception as e:
            logger.error(f"Error in getEmbeddingsFromDocuments: {e}", exc_info=True)
            raise

    def embeddingsSearch(self, query: str = string, documents: list[str] = documents):
        logger.info(f"embeddingsSearch method called with query (first 50 chars): '{query[:50]}' and {len(documents)} documents.")
        try:
            # Test the embeddings
            fact_embedding = self.huggingface_embeddings.embed_documents(documents)  # type: ignore[reportGeneralTypeIssues]
            question_embedding = self.huggingface_embeddings.embed_query(query)  # type: ignore[reportGeneralTypeIssues]
            logger.debug(f"Fact embedding length: {len(fact_embedding)}, Question embedding length: {len(question_embedding)}")

            result = cosine_similarity(np.array([question_embedding]), np.array(fact_embedding))
            logger.debug(f"Cosine similarity calculation completed. Result shape: {result.shape}")

            sorted_list = [
                f"{x:.4f} ({documents[i]})"
                for rank, (i, x) in enumerate(
                    sorted(enumerate(result.tolist()[0]), key=lambda y: y[1], reverse=True)[
                        :3
                    ]
                )
            ]
            logger.info("embeddingsSearch completed successfully.")
            return sorted_list
        except Exception as e:
            logger.error(f"Error in embeddingsSearch: {e}", exc_info=True)
            raise
