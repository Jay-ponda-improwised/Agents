from rich.markdown import Markdown
from utility.Console.Base import MarkdownComponent

class TextBlock(MarkdownComponent):
    """
    A component for paragraph text that supports Markdown.
    """

    def __init__(self, data: str, point: bool = False):
        super().__init__(data)
        self.point = point

    def bind(self) -> Markdown:
        if self.point:
            return Markdown(f"- {self.data}")
        return Markdown(self.data)
