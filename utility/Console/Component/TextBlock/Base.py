from rich.markdown import Markdown
from utility.Console.Base import MarkdownComponent

class TextBlock(MarkdownComponent):
    """
    A component for paragraph text that supports Markdown.
    """

    def __init__(self, data: str):
        super().__init__(data)

    def bind(self) -> Markdown:
        return Markdown(self.data)
