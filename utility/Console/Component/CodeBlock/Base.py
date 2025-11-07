from rich.panel import Panel
from rich.syntax import Syntax
from rich.style import Style
from utility.Console.Base import MarkdownComponent
from typing import Dict, Any
from rich import box

class CodeBlock(MarkdownComponent):
    """
    A component for code blocks.
    """

    def __init__(self, code: str, language: str = "text", title: str = "Code"):
        super().__init__(code)
        self.language = language
        self.title = title

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the component.
        """
        return {
            "id": self._id,
            "type": self.__class__.__name__,
            "code": self.data,
            "language": self.language,
            "title": self.title
        }

    def bind(self) -> Panel:
        syntax = Syntax(
            self.data, self.language, theme="monokai", line_numbers=True, word_wrap=True
        )
        return Panel(
            syntax,
            title=self.title,
            title_align="left",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(0, 1),
            style=Style(color="yellow", bold=True),
        )
