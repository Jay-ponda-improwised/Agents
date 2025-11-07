from rich.text import Text
from rich.style import Style
from utility.Console.Base import MarkdownComponent

class SubTopic(MarkdownComponent):
    """
    A component for H4 titles.
    """

    def bind(self) -> Text:
        return Text(f"➡ {self.data}", style=Style(color="green", bold=True, underline=True))
