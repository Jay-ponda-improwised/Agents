from rich.text import Text
from rich.style import Style
from rich.console import Group
from rich.rule import Rule
from utility.Console.Base import MarkdownComponent

class Topic(MarkdownComponent):
    """
    A component for H3 titles.
    """

    def bind(self) -> Group:
        topic_text = Text(f"● {self.data}", style=Style(color="cyan", bold=True))
        topic_rule = Rule(style=Style(color="cyan"))
        return Group(topic_text, topic_rule)
