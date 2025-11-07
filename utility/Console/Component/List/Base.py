from typing import List as PyList, Union, Any
from rich.text import Text
from rich.console import Group
from utility.Console.Base import MarkdownParentComponent, MarkdownComponent

class ListComponent(MarkdownParentComponent):
    def __init__(self, items: PyList[Union[str, int, float, bool, PyList[Any], MarkdownComponent]], ordered: bool = False, level: int = 1):
        processed_items = []
        for item in items:
            if isinstance(item, PyList):
                # Recursively create a new ListComponent for the nested list
                processed_items.append(ListComponent(item, ordered=ordered, level=level + 1))
            else:
                processed_items.append(item)

        super().__init__(data=processed_items)
        self.items = processed_items
        self.ordered = ordered
        self.level = level

    def bind(self):
        list_items = []
        for i, item in enumerate(self.items):
            if isinstance(item, str):
                prefix = f"{i + 1}." if self.ordered else "➤"
                list_items.append(Text(f"{'  ' * (self.level - 1)}{prefix} {item}"))
            elif isinstance(item, ListComponent):
                item.level = self.level + 1
                list_items.append(item.bind())
            elif isinstance(item, MarkdownComponent):
                list_items.append(item.bind())
            else: # Handle any other data type by converting it to a string
                prefix = f"{i + 1}." if self.ordered else "➤"
                list_items.append(Text(f"{'  ' * (self.level - 1)}{prefix} {str(item)}"))

        for child in self.children:
            if isinstance(child, ListComponent):
                child.level = self.level + 1
            list_items.append(child.bind())

        return Group(*list_items)
