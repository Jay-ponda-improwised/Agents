from rich.markdown import Markdown
from rich.text import Text
from typing import Union
from utility.Console.Base import MarkdownComponent

class TextBlock(MarkdownComponent):
    """
    A component for paragraph text that supports Markdown.
    """

    def __init__(self, data: str, point: bool = False):
        super().__init__(data)
        self.point = point

    def bind(self) -> Union[Markdown, Text]:
        if not self.data.strip():
            return Text("")
        if self.point:
            return Markdown(f"- {self.data}")
        return Markdown(self.data)
