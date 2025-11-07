from rich.text import Text
from rich.style import Style
from utility.Console.Base import MarkdownComponent

class MainTitle(MarkdownComponent):
    """
    A component for H1 titles.
    """

    def bind(self) -> Text:
        return Text(self.data, style=Style(color="hot_pink", bold=True, underline=True))
