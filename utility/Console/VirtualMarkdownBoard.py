"""
VirtualMarkdownBoard module for creating a virtual markdown board.
"""
import json
from typing import List, Optional, Dict, Any, Union
from rich.markdown import Markdown
from rich.console import Console, Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich import box
from rich.style import Style
from rich.table import Table

from utility.Console.Base import MarkdownComponent
from utility.Console.Component.MainTitle.Base import MainTitle
from utility.Console.Component.SubTitle.Base import SubTitle
from utility.Console.Component.Topic.Base import Topic
from utility.Console.Component.SubTopic.Base import SubTopic
from utility.Console.Component.TextBlock.Base import TextBlock
from utility.Console.Component.CodeBlock.Base import CodeBlock
from utility.Console.Component.Table.Base import TableComponent
from utility.Console.Component.List.Base import ListComponent
from utility.Console.Component.Line.Base import LineComponent
from utility.Console.MarkdownComponentMissingError import MarkdownComponentMissingError


class VirtualMarkdownBoard:
    """
    A utility class for creating a virtual markdown board.
    """

    def __init__(self):
        self.components: List[str] = []
        self.component_map: Dict[str, MarkdownComponent] = {}
        self.console = Console()

    def has_component(self, component_id: str) -> bool:
        """
        Checks if a component with the given ID exists.
        """
        return component_id in self.component_map

    def get_component(self, component_id: str) -> MarkdownComponent:
        """
        Retrieves a component by its ID.
        """
        if not self.has_component(component_id):
            raise MarkdownComponentMissingError(f"Component with id '{component_id}' not found.")
        return self.component_map[component_id]

    def _add_component(self, component: MarkdownComponent) -> str:
        """
        Adds a component to the board.
        """
        component_id = component.get_id()
        self.components.append(component_id)
        self.component_map[component_id] = component
        return component_id

    def _handle_add_or_replace(self, new_component: MarkdownComponent, component_id: Optional[str]) -> str:
        """
        Handles adding a new component or replacing an existing one.
        """
        if component_id:
            if not self.has_component(component_id):
                raise MarkdownComponentMissingError(f"Component with id '{component_id}' not found.")
            self.replace_component(component_id, new_component)
            return new_component.get_id()
        return self._add_component(new_component)

    def main_title(self, text: str, component_id: Optional[str] = None) -> str:
        """
        Adds or replaces an H1 title.
        """
        return self._handle_add_or_replace(MainTitle(text), component_id)

    def sub_title(self, text: str, component_id: Optional[str] = None) -> str:
        """
        Adds or replaces an H2 title.
        """
        return self._handle_add_or_replace(SubTitle(text), component_id)

    def topic(self, text: str, component_id: Optional[str] = None) -> str:
        """
        Adds or replaces an H3 title.
        """
        return self._handle_add_or_replace(Topic(text), component_id)

    def sub_topic(self, text: str, component_id: Optional[str] = None) -> str:
        """
        Adds or replaces an H4 title.
        """
        return self._handle_add_or_replace(SubTopic(text), component_id)

    def text(self, text: str, point: bool = False, component_id: Optional[str] = None) -> str:
        """
        Adds or replaces a text block.
        """
        return self._handle_add_or_replace(TextBlock(text, point=point), component_id)

    def code_block(
        self,
        code: str,
        language: str = "text",
        title: str = "Code",
        component_id: Optional[str] = None,
    ) -> str:
        """
        Adds or replaces a code block.
        """
        return self._handle_add_or_replace(CodeBlock(code, language, title), component_id)

    def table(
        self,
        headers: List[str],
        rows: List[List[str]],
        first_column_as_header: bool = True,
        add_column_number: bool = False,
        component_id: Optional[str] = None,
    ) -> str:
        """
        Adds or replaces a table.
        """
        return self._handle_add_or_replace(TableComponent(headers, rows, first_column_as_header, add_column_number), component_id)

    def list(
        self,
        items: List[Union[str, List[Any], MarkdownComponent]],
        ordered: bool = False,
        level: int = 1,
        component_id: Optional[str] = None,
    ) -> str:
        """
        Adds or replaces a list.
        """
        return self._handle_add_or_replace(
            ListComponent(items, ordered, level), component_id
        )

    def line(
        self,
        style: Optional[str] = "default",
        character: str = "─",
        component_id: Optional[str] = None,
    ) -> str:
        """
        Adds or replaces a horizontal line.
        """
        return self._handle_add_or_replace(
            LineComponent(style, character), component_id
        )

    def replace_component(self, component_id: str, new_component: MarkdownComponent):
        """
        Replaces a component on the board.
        """
        if not self.has_component(component_id):
            raise MarkdownComponentMissingError(f"Component with id '{component_id}' not found.")

        # Replace in the list
        new_component_id = new_component.get_id()
        for i, comp_id in enumerate(self.components):
            if comp_id == component_id:
                self.components[i] = new_component_id
                break

        # Replace in the map
        del self.component_map[component_id]
        self.component_map[new_component_id] = new_component

    def take_snapshot(self, title: str = "Markdown Output"):
        """
        Renders the board to the console.
        """
        renderables = [self.component_map[comp_id].bind() for comp_id in self.components]
        content_group = Group(*renderables)

        panel = Panel(
            content_group,
            title=title,
            title_align="left",
            border_style="yellow",
            padding=(1, 2),
            box=box.ROUNDED,
        )
        self.console.print(panel)

    def remove_snapshot(self):
        """
        Clears the board.
        """
        self.components = []
        self.component_map = {}
