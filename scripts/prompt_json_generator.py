import re
from langchain_core.prompts import PromptTemplate
from service.model_service import convert_prompt


template_string = """
    Index: 
        1. Description
        2. Rules
        3. Response rule
        3. Content to summarize
    ---
    1. Description:
        Summarize the following content in {max_length} characters. Format the response as {response_format}. follow the below rules:
    ----
    2. Rules:
    - Response must be in valid json format.
        - it must have key named as "response_format" = {response_format}.
        - it must have key named as "title" = title of summary evaluated from content.
        - it must have key named as "summary" = actual summary.
    - Use bullet points for lists when appropriate.
    - Summarize only the main points clearly and objectively.
    - Do not add any commentary, opinions, or extra information.
    - NEVER USE OTHER THEN ENGLISH LANGUAGE.
    ---
    3. Response rule {response_format}:
    {rules}
    ---
    4. Content to summarize:
    {content}
"""



template = PromptTemplate(
    input_variables=["content", "max_length", "response_format", "rules"],
    template=convert_prompt(template_string),
    validate_template=True,
    name="summarize_prompt_template",
)

template.save("templates/summarize_prompt_template.json")
