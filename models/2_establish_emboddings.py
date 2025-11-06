"""
this code demonstrate to the user how to establish communication between
the script and the remote llm server provider.
"""

from langchain_openai import OpenAIEmbeddings
from constants.config import (
    KEY,
    HOST,
    MODEL_QUEN,
    MAX_TIME_TO_WAIT,
    RETRIES,
    MODEL_QUEN_EMBEDDINGS,
)
import json
from constants.singleton import styler

import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key=MODEL_QUEN_EMBEDDINGS,
)

result = client.feature_extraction(
    """
        {                                                                             
            "biological": "Parrots have specialized vocal organs called syrinx that allow them to mimic sounds and human speech.",                                        
            "social": "They use talking as a form of social bonding and communication within their flock or with humans.",                                                   
            "intelligence": "Parrots are highly intelligent birds that can learn and repeat words to interact with their environment.",                                     
            "territorial": "Vocal mimicry helps them establish territory and communicate with other birds in the wild.",                                                 
            "entertainment": "Pet parrots often talk to entertain themselves and gain attention from their human companions."                                         
        }      
    """.replace(
        r"[ \n\t\r]+", " "
    ).strip(),
    model="Qwen/Qwen3-Embedding-0.6B",
)

# model = OpenAIEmbeddings(
#     model=MODEL_QUEN,
#     api_key=KEY,
#     base_url=HOST,
#     skip_empty=True,
#     timeout=MAX_TIME_TO_WAIT,
#     retry_max_seconds=MAX_TIME_TO_WAIT,
#     max_retries=RETRIES,
#     chunk_size=64,
#     dimensions=32,
# )

# result = model.embed_query(
#     """
#         {
#             "biological": "Parrots have specialized vocal organs called syrinx that allow them to mimic sounds and human speech.",
#             "social": "They use talking as a form of social bonding and communication within their flock or with humans.",
#             "intelligence": "Parrots are highly intelligent birds that can learn and repeat words to interact with their environment.",
#             "territorial": "Vocal mimicry helps them establish territory and communicate with other birds in the wild.",
#             "entertainment": "Pet parrots often talk to entertain themselves and gain attention from their human companions."
#         }
#     """.replace(
#         r"[ \n\t\r]+", " "
#     ).strip()
# )

print(result)

# Display the response using the utility class.rint_markdown_panel(json.dumps(response), title="Parrot Talk Response")
