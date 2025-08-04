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
