"""
Utility module for Rich library styling that can be reused across the project.
"""

import json
from typing import Optional, Match, List, Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.syntax import Syntax
from rich import box
import re


class RichStyler:
    """A utility class for consistent Rich library styling across the project."""

    def __init__(self):
        self.console = Console()

        # Define default styles
        self.default_md_style = Style(color="white")
        self.default_border_style = "yellow"
        self.default_title_style = Style(color="yellow", bold=True)

        # Define H1 styles
        self.h1_style = Style(color="hot_pink", bold=True, underline=True)

        # Code block styles
        self.code_block_style = Style(bgcolor="black", color="white")
        self.code_panel_style = Style(color="yellow", bold=True)
        self.code_border_style = "cyan"

    def _process_code_blocks(self, content: str) -> str:
        """
        Process markdown content to wrap code blocks in Rich panels with rounded corners.

        Args:
            content (str): The markdown content to process

        Returns:
            str: Processed content with code blocks wrapped in panel markers
        """
        # Pattern to match code blocks in markdown (```language\ncode\n```)
        code_block_pattern = r"```(\w+)?\n(.*?)```"

        def replace_code_block(match: Match[str]) -> str:

            # Return a placeholder that we'll replace with the actual panel
            # We use a unique marker that won't appear in normal text
            return f"<!--CODE_PANEL:{len(match.group(0))}-->"

        # Replace code blocks with placeholders
        processed_content = re.sub(
            code_block_pattern, replace_code_block, content, flags=re.DOTALL
        )

        # For now, we return the processed content with placeholders
        # In a more advanced implementation, you might want to handle the actual rendering
        return processed_content

    def print_markdown_panel(
        self,
        content: str,
        title: str = "Response",
        md_style: Optional[Style] = None,
        border_style: Optional[str] = None,
        title_style: Optional[Style] = None,
    ) -> None:
        """
        Print content in a Markdown panel with custom styling.

        Args:
            content (str): The content to display
            title (str): The panel title
            md_style (Style): Custom style for Markdown content
            border_style (str): Custom border style
            title_style (Style): Custom title style
        """
        # Use default styles if custom ones aren't provided
        md_style = md_style or self.default_md_style
        border_style = border_style or self.default_border_style
        title_style = title_style or self.default_title_style

        # Process content to handle code blocks separately
        final_content = self._render_content_with_code_panels(content)

        # Create the main panel
        panel = Panel(
            final_content,
            title=title,
            title_align="left",
            border_style=border_style,
            padding=(1, 2),
            box=box.ROUNDED,
        )

        # Print to console
        self.console.print(panel)

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
            return Markdown(content, style=self.default_md_style, code_theme="monokai")

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
                            parts[i], style=self.default_md_style, code_theme="monokai"
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

    def print_code_block(self, code: str, language: str = "text", title: str = "Code"):
        """
        Print a standalone code block with rounded corners border.

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

        self.console.print(code_panel)

    def print_styled_text(
        self,
        content: str,
        style: Optional[Style] = None,
        italic: bool = False,
        underline: bool = False,
    ) -> None:
        """
        Print styled text directly.

        Args:
            content (str): The text to display
            style (Style): Custom style for the text
            italic (bool): Whether to apply italic formatting
            underline (bool): Whether to apply underline formatting
        """
        # Apply additional styles if requested
        if italic:
            content = f"[italic]{content}[/italic]"
        if underline:
            content = f"[underline]{content}[/underline]"

        # Create Text object with style
        text = Text(content, style=style or self.default_md_style)

        # Print to console
        self.console.print(text)

    def print_success(self, message: str):
        """Print a success message with standard styling."""
        self.print_styled_text(
            f"✓ {message}", style=Style(color="green", bold=True)
        )

    def print_error(self, message: str):
        """Print an error message with standard styling."""
        self.print_styled_text(
            f"✗ {message}", style=Style(color="red", bold=True)
        )

    def print_warning(self, message: str):
        """Print a warning message with standard styling."""
        self.print_styled_text(
            f"⚠ {message}", style=Style(color="yellow", bold=True)
        )

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
