# MCP Server - Simple Demo

This is a minimal MCP (Model Context Protocol) server that provides basic tools for AI agents to consume.

## What It Does

The server provides two simple tools:
- **hello(name)**: Returns a personalized greeting
- **get_current_datetime(format)**: Returns current date/time in specified format

## Server Code

```python
#!/usr/bin/env python3
"""Simplest MCP Server"""

from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-server")

@mcp.tool()
def hello(name: str = "World") -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"

@mcp.tool()
def get_current_datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Get the current date and time in the specified format"""
    return datetime.now().strftime(format)

if __name__ == "__main__":
    mcp.run()
```

## Setup

```bash
uv sync
```

## Running the Server

### Option 1: Direct Run
```bash
python mcp_server/server.py
```

### Option 2: With MCP Inspector (Recommended)
```bash
mcp-inspector python mcp_server/server.py
```

## Testing with MCP Inspector

1. Install MCP Inspector: `npm install -g @modelcontextprotocol/inspector`
2. Run: `mcp-inspector python mcp_server/server.py`
3. Browser opens at http://localhost:6274
4. Test the tools:
   - **hello**: Try with different names
   - **get_current_datetime**: Try with different format strings

## Available Tools

### hello(name: str = "World") -> str
- **Description**: Say hello to someone
- **Parameters**: `name` (optional, default: "World")
- **Example**: `hello("Alice")` → `"Hello, Alice!"`

### get_current_datetime(format: str = "%Y-%m-%d %H:%M:%S") -> str
- **Description**: Get current date and time in specified format
- **Parameters**: `format` (optional, default: "%Y-%m-%d %H:%M:%S")
- **Examples**: 
  - `get_current_datetime()` → `"2025-01-03 20:28:09"`
  - `get_current_datetime("%Y-%m-%d")` → `"2025-01-03"`
  - `get_current_datetime("%H:%M:%S")` → `"20:28:09"`

## Key Features

- **FastMCP Framework**: Modern, simple MCP server implementation
- **Type Safety**: Full type hints for parameters and return values
- **Auto Documentation**: Docstrings become tool descriptions
- **Easy Testing**: Works with MCP Inspector out of the box
