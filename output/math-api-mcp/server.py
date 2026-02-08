from __future__ import annotations
import asyncio, json, os
from typing import Any
import httpx
from dedalus_mcp import MCPServer, tool

BASE_URL = os.getenv("BASIC_MATH_API_BASE_URL", "http://127.0.0.1:8001")
API_KEY = os.getenv("BASIC_MATH_API_API_KEY", "")

def _headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    if API_KEY:
        h["Authorization"] = f"Bearer {API_KEY}"
    return h

async def _request(method: str, path: str, *, params: dict[str, Any] | None = None,
                   body: dict[str, Any] | None = None) -> str:
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.request(method, url, headers=_headers(),
                                      params=params, json=body if body else None)
            resp.raise_for_status()
            try:
                return json.dumps(resp.json(), indent=2)
            except Exception:
                return resp.text
        except httpx.HTTPStatusError as e:
            return json.dumps({"error": str(e), "status": e.response.status_code})
        except Exception as e:
            return json.dumps({"error": str(e)})

@tool(description="Add two numbers [WRITES DATA]")
async def addnumbers(a: float, b: float) -> str:
    """Add two numbers."""
    return await _request("POST", "/add", body={"a": a, "b": b})

@tool(description="Divide two numbers [WRITES DATA]")
async def dividenumbers(a: float, b: float) -> str:
    """Divide two numbers."""
    return await _request("POST", "/divide", body={"a": a, "b": b})

@tool(description="Health check")
async def healthcheck() -> str:
    """Health check."""
    return await _request("GET", "/health")

@tool(description="Multiply two numbers [WRITES DATA]")
async def multiplynumbers(a: float, b: float) -> str:
    """Multiply two numbers."""
    return await _request("POST", "/multiply", body={"a": a, "b": b})

@tool(description="Subtract two numbers [WRITES DATA]")
async def subtractnumbers(a: float, b: float) -> str:
    """Subtract two numbers."""
    return await _request("POST", "/subtract", body={"a": a, "b": b})

server = MCPServer("math-api")
server.collect(addnumbers, dividenumbers, healthcheck, multiplynumbers, subtractnumbers)
if __name__ == "__main__":
    asyncio.run(server.serve())