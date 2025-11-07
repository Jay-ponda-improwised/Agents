from rich.rule import Rule
from rich.style import Style
from typing import Optional
from utility.Console.Base import MarkdownComponent

class LineComponent(MarkdownComponent):
    """
    A component for drawing a horizontal line.
    """
    def __init__(self, style: Optional[str] = "default", character: str = "─"):
        super().__init__(data={"style": style, "character": character})
        self.style = style
        self.character = character

    def bind(self) -> Rule:
        return Rule(style=self.style, characters=self.character)
