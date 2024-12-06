from dataclasses import dataclass
from typing import Callable, Optional
from llama_index.core.tools import ToolMetadata

from enum import Enum

class ToolType(Enum):
    """
    Enum to represent the type of tools.
    """
    QUERY_ENGINE = "query_engine"
    FUNCTION = "function"
    
@dataclass
class ToolInfo:
    """
    Represents the information required to create a tool.
    """
    tool_type: ToolType  # Use ToolType enum instead of plain string
    metadata: Optional[ToolMetadata] = None  # Metadata for query engine tools
    query_engine: Optional[object] = None  # Query engine instance (for query tools)
    fn: Optional[Callable] = None  # Function (for function tools)
    name: Optional[str] = None  # Name of the function (for function tools)