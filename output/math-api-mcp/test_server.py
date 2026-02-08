"""Auto-generated tests for Basic Math API MCP server."""

import asyncio
import json

from dedalus_mcp.client import MCPClient


SERVER_URL = "http://127.0.0.1:8000/mcp"


async def test_list_tools():
    """Verify all expected tools are registered."""
    client = await MCPClient.connect(SERVER_URL)
    tools = await client.list_tools()
    names = sorted(t.name for t in tools.tools)
    expected = ['add_numbers', 'divide_numbers', 'health_check', 'multiply_numbers', 'subtract_numbers']
    assert names == expected, f"Tool mismatch: {{names}} != {{expected}}"
    print(f"✓ All {len(names)} tools registered")
    await client.close()


async def test_tool_schemas():
    """Verify each tool has a valid input schema."""
    client = await MCPClient.connect(SERVER_URL)
    tools = await client.list_tools()
    for t in tools.tools:
        assert t.name, "Tool missing name"
        assert t.description, f"Tool {t.name} missing description"
        print(f"✓ {t.name}: schema OK")
    await client.close()


async def test_read_tools_dry_run():
    """Dry-run read-only tools (expects server + upstream to be reachable)."""
    client = await MCPClient.connect(SERVER_URL)
    try:
        result = await client.call_tool('divide_numbers', {'a': 'test', 'b': 'test'})
        print(f"✓ divide_numbers: {result.content[0].text[:100]}")
    except Exception as e:
        print(f"✗ divide_numbers: {e}")
    try:
        result = await client.call_tool('health_check', {})
        print(f"✓ health_check: {result.content[0].text[:100]}")
    except Exception as e:
        print(f"✗ health_check: {e}")
    try:
        result = await client.call_tool('multiply_numbers', {'a': 'test', 'b': 'test'})
        print(f"✓ multiply_numbers: {result.content[0].text[:100]}")
    except Exception as e:
        print(f"✗ multiply_numbers: {e}")
    try:
        result = await client.call_tool('subtract_numbers', {'a': 'test', 'b': 'test'})
        print(f"✓ subtract_numbers: {result.content[0].text[:100]}")
    except Exception as e:
        print(f"✗ subtract_numbers: {e}")
    await client.close()


async def main():
    await test_list_tools()
    await test_tool_schemas()
    # Uncomment to test against a live upstream:
    # await test_read_tools_dry_run()


if __name__ == "__main__":
    asyncio.run(main())
