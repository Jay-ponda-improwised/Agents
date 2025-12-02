import logging
from enum import Enum
from langchain_core.prompts import PromptTemplate
from service.model_service import get_model_service
from config.enums import ModelName
from langchain_openai import ChatOpenAI
from typing import cast


logger = logging.getLogger(__name__)


class ResponseLengthOptions(Enum):
    SHORT = "SHORT"
    MEDIUM = "MEDIUM"
    LONG = "LONG"

    @property
    def description(self):
        descriptions = {
            "SHORT": "SHORT (1 paragraph, 3-4 sentences, approx. 100 words)",
            "MEDIUM": "MEDIUM (2-3 paragraphs, 8-10 sentences, approx. 100-300 words)",
            "LONG": "LONG (6-7 paragraphs, 15-20 sentences, approx. 300-500 words)",
        }
        return descriptions.get(
            self.value, "MEDIUM (2-3 paragraphs, 8-10 sentences, approx. 100-300 words)"
        )

    @property
    def max_tokens(self):
        max_tokens_map = {
            "SHORT": 256,
            "MEDIUM": 1024,
            "LONG": 4112,
        }
        return max_tokens_map.get(self.value, 300)


class ResponseFormatOptions(Enum):
    PLAIN_TEXT = "PLAIN_TEXT"
    MARKDOWN = "MARKDOWN"
    JSON = "JSON"
    CODE = "CODE"

    @property
    def description(self):
        descriptions = {
            "PLAIN_TEXT": "plain text",
            "MARKDOWN": "markdown",
            "JSON": "json",
            "CODE": "{relevant programming language}",
        }
        return descriptions.get(self.value, "plain text")

    @property
    def rules(self):
        descriptions = {
            "PLAIN_TEXT": """
                - Provide the summary in plain text format without any special formatting.
            """,
            "MARKDOWN": """
                - Format the summary using Markdown syntax, including headings, lists, and emphasis where appropriate.
                - Use bold (`**bold**`) and italic (`*italic*`) formatting for emphasis.
                - Use numbered lists for sequential steps or items, Use unordered lists for non-sequential items or bullet points.
                - Use horizontal lines (---) to separate sections.
            """,
            "JSON": """
                - Structure the summary as a valid JSON object.
                - Use key-value pairs to represent different sections or points of the summary.
                - Ensure proper nesting of objects and arrays where necessary.
            """,
            "CODE": """
                - Include code snippets within triple backticks (```) if applicable.
                - Specify the relevant programming language after the opening triple backticks (I.E. ```python).
                - Ensure the code is properly indented and formatted.
                - Avoid using excessive indentation or tabs for code blocks.
            """,
        }
        return descriptions.get(self.value, "plain text")


class DemoPromptService:

    def __init__(self):
        logger.info("DemoPromptService initialized.")
        model_service = get_model_service()
        model = model_service.get_model(ModelName.OPENAI_CHAT)
        if not model:
            raise RuntimeError("Failed to get model from ModelService")

        self.model_instance = cast(ChatOpenAI, model)
        self.template = PromptTemplate(
            input_variables=["content", "max_length", "response_format", "rules"],
            template="""
                Index: 
                    1. description
                    2. rules
                    3. response rule
                    3. content to summarize
                ---
                1. Description:
                    Summarize the following content in {max_length} characters. Format the response as {response_format}. follow the below rules:
                ----
                2. Rules:
                - Begin the response with ```{response_format} followed by the summary.
                - Use bullet points for lists when appropriate.
                - Summarize only the main points clearly and objectively.
                - Do not add any commentary, opinions, or extra information.
                - NEVER USE OTHER THEN ENGLISH LANGUAGE.
                ---
                3. Response rule {response_format}:
                {rules}
                ---
                4. Content:
                {content}
            """.replace(
                "[ \n\t\r]", " "
            ).strip(),
            validate_template=True,
        )

    def getSummarizePrompt(
        self,
        max_length: ResponseLengthOptions,
        response_format: ResponseFormatOptions,
        content: str,
    ) -> str:
        logger.info(
            f"Generating summarize prompt. max_length: {max_length.value}, response_format: {response_format.value}, content: {content}"
        )
        prompt = self.template.invoke(
            {
                "content": content,
                "max_length": max_length.description,
                "response_format": response_format.description,
                "rules": response_format.rules,
            }
        )
        logger.debug(f"Generated prompt: {prompt}")

        response = self.model_instance.invoke(prompt, max_tokens=max_length.max_tokens)
        logger.debug(f"Received response: {response}")

        if isinstance(response.content, str):
            return response.content

        return str(response.content)
