"""Auto-generated MCP server for Basic Math API.

API version: 1.0.0
Base URL: http://127.0.0.1:8001
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx
from dedalus_mcp import MCPServer, tool


# ── Configuration ────────────────────────────────────────────────────────────

BASE_URL = os.getenv("BASIC_MATH_API_BASE_URL", "http://127.0.0.1:8001")
API_KEY = os.getenv("BASIC_MATH_API_API_KEY", "")


def _headers() -> dict[str, str]:
    h: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if API_KEY:
        h["Authorization"] = f"Bearer {API_KEY}"
    return h


async def _request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
) -> str:
    """Make an HTTP request to the upstream API."""
    url = f"{BASE_URL}{path}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request(
            method,
            url,
            headers=_headers(),
            params=params,
            json=body if body else None,
        )
        resp.raise_for_status()
        try:
            data = resp.json()
            return json.dumps(data, indent=2)
        except Exception:
            return resp.text


# ── Tools ────────────────────────────────────────────────────────────────────


@tool(description='Calculates the sum of two numbers. [WRITES DATA]')
async def add_numbers(a: float, b: float) -> str:
    path = f"/add"
    body: dict[str, Any] = {}
    body["a"] = a
    body["b"] = b
    return await _request("POST", path, body=body)


@tool(description='Calculates the quotient of two numbers.')
async def divide_numbers(a: float, b: float) -> str:
    path = f"/divide"
    body: dict[str, Any] = {}
    body["a"] = a
    body["b"] = b
    return await _request("POST", path, body=body)


@tool(description='Checks the health status of the API.')
async def health_check() -> str:
    path = f"/health"
    return await _request("GET", path)


@tool(description='Calculates the product of two numbers.')
async def multiply_numbers(a: float, b: float) -> str:
    path = f"/multiply"
    body: dict[str, Any] = {}
    body["a"] = a
    body["b"] = b
    return await _request("POST", path, body=body)


@tool(description='Calculates the difference between two numbers.')
async def subtract_numbers(a: float, b: float) -> str:
    path = f"/subtract"
    body: dict[str, Any] = {}
    body["a"] = a
    body["b"] = b
    return await _request("POST", path, body=body)


# ── Server ───────────────────────────────────────────────────────────────────

server = MCPServer("math-api")
server.collect(add_numbers, divide_numbers, health_check, multiply_numbers, subtract_numbers)

if __name__ == "__main__":
    asyncio.run(server.serve())
