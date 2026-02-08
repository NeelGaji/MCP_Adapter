from __future__ import annotations
import asyncio
import json
from typing import Any
from dedalus_mcp.client import MCPClient
import pytest

async def test_list_tools():
    """Verify all 8 tools are registered."""
    client = await MCPClient.connect("http://127.0.0.1:8000/mcp")
    try:
        tools = await client.list_tools()
        assert len(tools) == 8, f"Expected 8 tools, got {len(tools)}"
    finally:
        await client.close()

async def test_tool_schemas():
    """Verify each tool has name and description."""
    client = await MCPClient.connect("http://127.0.0.1:8000/mcp")
    try:
        tools = await client.list_tools()
        for tool in tools:
            assert "name" in tool, f"Tool missing name: {tool}"
            assert "description" in tool, f"Tool missing description: {tool['name']}"
    finally:
        await client.close()

async def test_sample_tool_calls():
    """Test basic functionality of sample tools."""
    client = await MCPClient.connect("http://127.0.0.1:8000/mcp")
    try:
        # Test search_pets (should at least not error)
        result = await client.call_tool("search_pets", {})
        assert isinstance(json.loads(result), (dict, list)), "Invalid JSON response"
        
        # Test createpet schema (won't actually create without valid params)
        with pytest.raises(Exception):
            await client.call_tool("createpet", {"invalid": "params"})
    finally:
        await client.close()

async def main():
    """Run all test cases."""
    await test_list_tools()
    await test_tool_schemas()
    await test_sample_tool_calls()
    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(main())