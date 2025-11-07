import uuid
import json
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union

class MarkdownComponent(ABC):
    """
    Abstract base class for all markdown components.
    """

    def __init__(self, data: Any):
        self._id = str(uuid.uuid4())
        self.data = data

    def get_id(self) -> str:
        """
        Returns the unique ID of the component.
        """
        return self._id

    def get_data(self) -> Any:
        """
        Returns the data associated with the component.
        """
        return self.data

    def to_dict(self) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the component.
        """
        return {
            "id": self._id,
            "type": self.__class__.__name__,
            "data": self.data
        }

    def __str__(self) -> str:
        return str(self.to_dict())

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @abstractmethod
    def bind(self) -> Any:
        """
        Binds the component to a Rich renderable object.
        """
        pass

class MarkdownChildComponent(MarkdownComponent):
    """
    Abstract base class for child components.
    """
    def bind(self) -> Any:
        return self.data


class MarkdownParentComponent(MarkdownComponent):
    """
    Abstract base class for parent components.
    """
    def __init__(self, data: Any):
        super().__init__(data)
        self.children: List[MarkdownChildComponent] = []

    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        return base_dict


class ShellowMarkdownChildComponent(MarkdownChildComponent):
    """
    Abstract base class for singleton child components that provide styles and formatted data.
    """

    def __init__(self):
        super().__init__(data=None)

    def bind(self) -> Any:
        return None

