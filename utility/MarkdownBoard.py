"""
MarkdownBoard module for creating markdown content using Rich library styling.
"""
import re
import json
from typing import List, Union, Optional, Match, Any
from rich.console import Console, Group
from rich.text import Text
from rich.style import Style
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich import box
from utility.rich_styler import RichStyler


class TableComponent:
    """Base class for table components."""
    pass


class TableHeader(TableComponent):
    """Represents a table header cell."""
    def __init__(self, content: str):
        self.content = content


class TableData(TableComponent):
    """Represents a table data cell."""
    def __init__(self, content: str):
        self.content = content


class TableRow:
    """Represents a table row."""
    def __init__(self, cells: List[Union[TableHeader, TableData]]):
        self.cells = cells


class MarkdownBoard:
    """A utility class for creating markdown content with styling."""
    
    def __init__(self):
        self.console = Console()
        self.content_parts = []
        self.rich_styler = RichStyler()
        
        # Define styles
        self.h1_style = Style(color="hot_pink", bold=True, underline=True)
        self.h2_style = Style(color="yellow", bold=True)
        self.h3_style = Style(color="cyan", bold=True)
        self.h4_style = Style(color="green", bold=True)
        self.link_style = Style(color="blue", underline=True)
        
        # Code block styles
        self.code_block_style = Style(bgcolor="black", color="white")
        self.code_panel_style = Style(color="yellow", bold=True)
        self.code_border_style = "cyan"
        
    def _format_json_in_markdown(self, content: str) -> str:
        """
        Format JSON content in markdown with 4-space indentation.
        
        Args:
            content (str): The markdown content to process
            
        Returns:
            str: Processed content with properly formatted JSON
        """
        # Pattern to match JSON code blocks in markdown (```json\n...\n```)
        json_block_pattern = r"```json\s*\n(.*?)\n\s*```"
        
        def format_json_block(match: Match[str]) -> str:
            try:
                # Extract JSON content
                json_content = match.group(1)
                
                # Parse and reformat with 4-space indentation
                parsed_json = json.loads(json_content)
                formatted_json = json.dumps(parsed_json, indent=4)
                
                # Return formatted JSON in code block
                return f"```json\n{formatted_json}\n```"
            except json.JSONDecodeError:
                # If JSON is invalid, return as is
                return match.group(0)
        
        # Replace JSON code blocks with formatted versions
        return re.sub(json_block_pattern, format_json_block, content, flags=re.DOTALL)
        
    def _render_content_with_code_panels(self, content: str) -> Any:
        """
        Render content with code blocks as separate panels.
        
        This method handles the actual rendering of code blocks as panels
        within the markdown content.
        """
        # Process JSON content to ensure proper formatting
        content = self._format_json_in_markdown(content)
        
        # Split content by code blocks
        parts = re.split(r"```(\w+)?\n(.*?)```", content, flags=re.DOTALL)
        
        if len(parts) == 1:
            # No code blocks found, return as simple Markdown
            return Markdown(content, style=Style(color="white"), code_theme="monokai")
        
        # We have code blocks, build a renderable group
        from rich.console import Group
        
        renderables: List[Any] = []
        
        i = 0
        while i < len(parts):
            if i % 3 == 0:
                # This is a text part (not a code block)
                if parts[i].strip():
                    renderables.append(
                        Markdown(
                            parts[i], style=Style(color="white"), code_theme="monokai"
                        )
                    )
            else:
                # This is a code block part (language + content)
                if i + 1 < len(parts):
                    language = parts[i] or "text"
                    code_content = parts[i + 1].strip()
                    
                    # Create syntax highlighted code
                    syntax = Syntax(
                        code_content,
                        language,
                        theme="monokai",
                        line_numbers=True,
                        word_wrap=True,
                    )
                    
                    # Create panel with rounded corners
                    code_panel = Panel(
                        syntax,
                        title=f"{language}",
                        title_align="center",
                        border_style=self.code_border_style,
                        box=box.ROUNDED,
                        padding=(0, 1),
                        style=self.code_panel_style,
                    )
                    
                    renderables.append(code_panel)
                    i += 1  # Skip the content part since we processed it
            i += 1
        
        return Group(*renderables)
        
    def writeCodeBlock(self, code: str, language: str = "text", title: str = "Code") -> None:
        """
        Write a standalone code block with rounded corners border.
        
        Args:
            code (str): The code content
            language (str): Programming language for syntax highlighting
            title (str): Panel title
        """
        syntax = Syntax(
            code, language, theme="monokai", line_numbers=True, word_wrap=True
        )
        
        code_panel = Panel(
            syntax,
            title=title,
            title_align="left",
            border_style=self.code_border_style,
            box=box.ROUNDED,
            padding=(0, 1),
            style=self.code_panel_style,
        )
        
        self.content_parts.append(code_panel)
        
    def writeMainTitle(self, text: str) -> None:
        """Write an H1 title."""
        title_text = Text(text, style=self.h1_style)
        self.content_parts.append(title_text)
        # Add a line after H1
        self.content_parts.append(Text(""))
        
    def writeSubTitle(self, text: str) -> None:
        """Write an H2 title."""
        title_text = Text(text, style=self.h2_style)
        self.content_parts.append(title_text)
        # Add a line after H2
        self.content_parts.append(Text(""))
        
    def writeTopic(self, text: str) -> None:
        """Write an H3 title."""
        title_text = Text(text, style=self.h3_style)
        self.content_parts.append(title_text)
        
    def writeSubTopic(self, text: str) -> None:
        """Write an H4 title."""
        title_text = Text(text, style=self.h4_style)
        self.content_parts.append(title_text)
        
    def writeText(self, text: str, bold: bool = False, italic: bool = False) -> None:
        """Write paragraph text with optional bold and italic formatting."""
        styled_text = text
        if bold and italic:
            styled_text = f"[bold][italic]{text}[/italic][/bold]"
        elif bold:
            styled_text = f"[bold]{text}[/bold]"
        elif italic:
            styled_text = f"[italic]{text}[/italic]"
            
        text_obj = Text.from_markup(styled_text)
        self.content_parts.append(text_obj)
        
    def writeList(self, items: List[str], ordered: bool = False, bold_items: Optional[List[bool]] = None, italic_items: Optional[List[bool]] = None) -> None:
        """Write a list (ordered or unordered) with optional bold and italic formatting for items."""
        bold_items = bold_items or [False] * len(items)
        italic_items = italic_items or [False] * len(items)
            
        for i, item in enumerate(items):
            is_bold = bold_items[i] if i < len(bold_items) else False
            is_italic = italic_items[i] if i < len(italic_items) else False
            
            styled_item = item
            if is_bold and is_italic:
                styled_item = f"[bold][italic]{item}[/italic][/bold]"
            elif is_bold:
                styled_item = f"[bold]{item}[/bold]"
            elif is_italic:
                styled_item = f"[italic]{item}[/italic]"
                
            prefix = f"{i+1}. " if ordered else "- "
            list_item = Text(prefix) + Text.from_markup(styled_item)
            self.content_parts.append(list_item)
            
    def writeLink(self, text: str, url: str) -> None:
        """Write a link with blue color and underline."""
        link_text = Text(text, style=self.link_style)
        # Make the link clickable in terminal that support it
        link_text.stylize(f"link {url}")
        self.content_parts.append(link_text)
        
    def writeTable(self, rows: List[TableRow], first_column_as_header: bool = False) -> None:
        """Write a table from TableRow objects.
        
        Args:
            rows: List of TableRow objects
            first_column_as_header: If True, highlight the first column as header
        """
        if not rows:
            return
            
        table = Table(show_header=True, header_style="bold magenta")
        
        # Add columns based on the first row (assuming it's headers)
        if rows and rows[0].cells:
            for i, cell in enumerate(rows[0].cells):
                if isinstance(cell, TableHeader):
                    table.add_column(cell.content)
                elif first_column_as_header and i == 0:
                    # Highlight first column as header if requested
                    table.add_column(cell.content, style="bold magenta")
                else:
                    table.add_column(cell.content)
                    
        # Add data rows
        for row in rows[1:]:
            cell_contents = []
            for i, cell in enumerate(row.cells):
                if first_column_as_header and i == 0:
                    # Highlight first column cells as header
                    cell_contents.append(f"[bold magenta]{cell.content}[/bold magenta]")
                else:
                    cell_contents.append(cell.content)
            table.add_row(*cell_contents)
            
        self.content_parts.append(table)
        
    def writeRow(self, cells: List[Union[TableHeader, TableData]]) -> TableRow:
        """Create a TableRow object."""
        return TableRow(cells)
        
    def writeColumns(self, content: str, is_header: bool = False) -> Union[TableHeader, TableData]:
        """Create a TableHeader or TableData object."""
        if is_header:
            return TableHeader(content)
        else:
            return TableData(content)
            
    def render(self) -> None:
        """Render all content to the console."""
        for part in self.content_parts:
            self.console.print(part)
            
    def TakeSnapshot(self, title: str = "Markdown Output") -> None:
        """Print everything as markdown in a panel, equivalent to print_markdown_panel."""
        # Print each content part directly using RichStyler's console
        # This ensures all content including code blocks and tables are rendered properly
        panel = Panel(
            Group(*self.content_parts),
            title=title,
            title_align="left",
            border_style="yellow",
            padding=(1, 2),
            box=box.ROUNDED,
        )
        
        self.rich_styler.console.print(panel)
        
    def RemoveSnapshot(self) -> None:
        """Reset variables to reuse the object."""
        self.content_parts = []
