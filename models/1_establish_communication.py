"""
this code demonstrate to the user how to establish communication between
the script and the remote llm server provider.
"""

import json
from langchain_openai import ChatOpenAI
from constants.config import (
    KEY,
    HOST,
    MODEL_QUEN,
    MAX_TIME_TO_WAIT,
    RETRIES,
    MAX_TOKENS,
)
from constants.singleton import styler

model = ChatOpenAI(
    model=MODEL_QUEN,
    api_key=KEY,
    base_url=HOST,
    temperature=0.7,
    seed=236,
    timeout=MAX_TIME_TO_WAIT,
    max_retries=RETRIES,
    max_completion_tokens=MAX_TOKENS,
    verbose=True,
    verbosity="medium",
)

response = model.invoke(
    f"""
        Why do parrots talk? 
        settings: 
        - in max 5 lines.
        - giving replay in raw markdown format. 
        - it should be in json format (json format should be structured and valid).
        - key will be topic and value will be the reason. (I.E. biological: he has something...) 
        - markdown code should have language information like ```<language> content... ``` (I.E. ```json {{}}```)
        - it should be consistent int one human language
    """
)

print(response)

# Display the response using the utility class
styler.print_markdown_panel(response.text, title="Parrot Talk Response")
