"""
this code demonstrate to the user how to establish communication between
the script and the remote llm server provider.
"""

import json
from constants.config import OLLAMA_HOST, MODEL_QUEN_EMBEDDINGS, ROOT_DIR
from constants.singleton import styler
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

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


# Initialize Ollama embeddings
embeddings = OllamaEmbeddings(
    model=MODEL_QUEN_EMBEDDINGS,
    base_url=OLLAMA_HOST,
)

# Test the embeddings
query_result = embeddings.embed_query(string)
print(f"Embedding dimension: {len(query_result)}")

styler.print_markdown_panel(json.dumps(query_result))

# For multiple documents
documents = [
    "Parrots have specialized vocal organs called syrinx that allow them to mimic sounds and human speech.",
    "They use talking as a form of social bonding and communication within their flock or with humans.",
    "Parrots are highly intelligent birds that can learn and repeat words to interact with their environment.",
    "Vocal mimicry helps them establish territory and communicate with other birds in the wild.",
    "Pet parrots often talk to entertain themselves and gain attention from their human companions.",
]
doc_embeddings = embeddings.embed_documents(documents)
print(f"Number of documents: {len(doc_embeddings)}")

styler.print_markdown_panel(json.dumps(doc_embeddings))


# hugging face
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder=ROOT_DIR + "/.cache",
    show_progress=True,
    model_kwargs={"device": "cpu"},
    query_encode_kwargs={"normalize_embeddings": True},
)

print(embeddings.embed_query(string))

styler.print_markdown_panel(json.dumps(embeddings.embed_query(string)))
