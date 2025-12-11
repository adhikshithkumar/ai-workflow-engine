from typing import Callable, Dict, Any

ToolFn = Callable[[Dict[str, Any]], Dict[str, Any]]

# A simple registry to store node functions
_tools: Dict[str, ToolFn] = {}


def register_tool(name: str, fn: ToolFn) -> None:
    """
    Register a tool function by name.
    """
    _tools[name] = fn


def get_tool(name: str) -> ToolFn:
    """
    Retrieve a tool by name. Raises error if not found.
    """
    if name not in _tools:
        raise KeyError(f"Tool '{name}' not registered")
    return _tools[name]
