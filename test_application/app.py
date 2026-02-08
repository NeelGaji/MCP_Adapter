"""Standalone Math REST API — a normal web app (non-MCP) that exposes
addition, subtraction, multiplication, and division via HTTP endpoints.

This is the "target software" that we will later wrap with an
auto-generated MCP adapter.

Swagger UI available at: http://127.0.0.1:8001/docs
OpenAPI spec at:         http://127.0.0.1:8001/openapi.json
"""

from __future__ import annotations

import json
from pathlib import Path

import uvicorn
import yaml
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route

_SPEC_PATH = Path(__file__).parent / "openapi.yaml"


# ── API handlers ───────────────────────────────────────────────────────────


async def add(request: Request) -> JSONResponse:
    data = await request.json()
    a, b = float(data["a"]), float(data["b"])
    return JSONResponse({"operation": "add", "a": a, "b": b, "result": a + b})


async def subtract(request: Request) -> JSONResponse:
    data = await request.json()
    a, b = float(data["a"]), float(data["b"])
    return JSONResponse({"operation": "subtract", "a": a, "b": b, "result": a - b})


async def multiply(request: Request) -> JSONResponse:
    data = await request.json()
    a, b = float(data["a"]), float(data["b"])
    return JSONResponse({"operation": "multiply", "a": a, "b": b, "result": a * b})


async def divide(request: Request) -> JSONResponse:
    data = await request.json()
    a, b = float(data["a"]), float(data["b"])
    if b == 0:
        return JSONResponse(
            {"operation": "divide", "a": a, "b": b, "error": "division by zero"},
            status_code=400,
        )
    return JSONResponse({"operation": "divide", "a": a, "b": b, "result": a / b})


async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok"})


# ── OpenAPI / Swagger UI ───────────────────────────────────────────────────


async def openapi_json(request: Request) -> JSONResponse:
    """Serve the OpenAPI spec as JSON (fetched from openapi.yaml)."""
    spec = yaml.safe_load(_SPEC_PATH.read_text(encoding="utf-8"))
    return JSONResponse(spec)


async def swagger_ui(request: Request) -> HTMLResponse:
    """Serve Swagger UI pointing at our /openapi.json."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Math API — Swagger UI</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: '/openapi.json',
      dom_id: '#swagger-ui',
      presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
      layout: 'BaseLayout',
    });
  </script>
</body>
</html>"""
    return HTMLResponse(html)


# ── App ────────────────────────────────────────────────────────────────────


app = Starlette(
    routes=[
        Route("/add", add, methods=["POST"]),
        Route("/subtract", subtract, methods=["POST"]),
        Route("/multiply", multiply, methods=["POST"]),
        Route("/divide", divide, methods=["POST"]),
        Route("/health", health, methods=["GET"]),
        Route("/openapi.json", openapi_json, methods=["GET"]),
        Route("/docs", swagger_ui, methods=["GET"]),
    ]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
