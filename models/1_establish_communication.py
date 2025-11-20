"""
this code demonstrate to the user how to establish communication between
the script and the remote llm server provider.
"""

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
from constants.singleton import styler

if not MODEL_QUEN:
    raise ValueError("MODEL_QUEN must be set in constants.config")
if not KEY:
    raise ValueError("KEY must be set in constants.config")

seed = random.randint(0, 999999)

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
        - Why do parrots talk?
        settings (must follow!):
        - in max 3 lines.
        - giving replay in raw markdown format.
        - it should be in json format (json format should be structured and valid).
        - key will be topic and value will be the reason. (I.E. biological: he has something...)
        - markdown code should have language information like ```<language> content... ``` (I.E. ```json {{}}```)
        - it should be consistent int one human language
    """
)

print(response)

# Display the response using the utility class
styler.print_markdown_panel(response.text, title=f"Parrot Talk Response ({seed})")
