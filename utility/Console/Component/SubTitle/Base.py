from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.rule import Rule
from utility.Console.Base import MarkdownComponent

class SubTitle(MarkdownComponent):
    """
    A component for H2 titles.
    """

    def bind(self) -> Group:
        return Group(
            Text(self.data, style=Style(color="yellow", bold=True, underline=True)),
            Rule(style=Style(color="yellow"))
        )
