from rich.text import Text
from rich.style import Style
from utility.Console.Base import MarkdownComponent

class Topic(MarkdownComponent):
    """
    A component for H3 titles.
    """

    def bind(self) -> Text:
        return Text(self.data, style=Style(color="cyan", bold=True))
