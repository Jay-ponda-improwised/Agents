from rich.text import Text
from rich.style import Style
from rich.prompt import Prompt
from utility.Console.Base import MarkdownComponent


class Input(MarkdownComponent):
    """
    A component for taking user input.
    """

    def __init__(self, prompt_text: str, password: bool = False):
        super().__init__(prompt_text)
        self.prompt_text = prompt_text
        self.password = password
        self._user_input = None

    def bind(self) -> Text:
        # Get user input using Rich's Prompt if not already obtained
        if self._user_input is None:
            try:
                if self.password:
                    self._user_input = Prompt.ask(self.prompt_text, password=True)
                else:
                    self._user_input = Prompt.ask(self.prompt_text)
            except EOFError:
                # Handle the case when running in non-interactive environment
                self._user_input = ""
        
        # Return a Text object showing the prompt and input (masked if password)
        if self.password:
            display_text = f"{self.prompt_text}: {'*' * len(self._user_input)}"
        else:
            display_text = f"{self.prompt_text}: {self._user_input}"
            
        return Text(display_text, style=Style(color="cyan"))