from rich.text import Text
from rich.style import Style
from utility.Console.Base import MarkdownComponent

class SubTitle(MarkdownComponent):
    """
    A component for H2 titles.
    """

    def bind(self) -> Text:
        return Text(self.data, style=Style(color="yellow", bold=True))
