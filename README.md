# MCP Adapter Generator

Turn any API into an AI-callable MCP server — automatically.

Point it at a **Swagger URL**, **OpenAPI spec**, or **Postman collection**, and it generates a production-ready [Dedalus MCP](https://docs.dedaluslabs.ai/dmcp) server with proper schemas, safety policies, and deployment files.

Optionally uses **AI reasoning** (K2 / Dedalus) to enhance tool names, descriptions, and parameter metadata.

---

## How It Works — The Full Workflow

```
  Swagger URL or file          AI Reasoning             Code Generation
  ┌──────────────┐   ┌──────────────┐   ┌────────────┐   ┌──────────────┐   ┌────────────┐
  │  1. INGEST   │──▶│ 2. MINE      │──▶│ 3. REASON  │──▶│ 4. SAFETY    │──▶│ 5. CODEGEN │
  │              │   │              │   │  (K2 / AI)  │   │              │   │            │
  │ Fetch spec   │   │ Cluster into │   │ Enhance     │   │ Classify     │   │ server.py  │
  │ from URL or  │   │ high-level   │   │ names,      │   │ read/write/  │   │ tests      │
  │ local file   │   │ tools        │   │ descriptions│   │ destructive  │   │ .env       │
  └──────────────┘   └──────────────┘   └────────────┘   └──────────────┘   └────────────┘
          │                                                                         │
          ▼                                                                         ▼
  http://host/openapi.json                                              output/my-server/
  examples/petstore.yaml                                                 ├── server.py
  collection.json                                                        ├── main.py
                                                                         ├── test_server.py
                                                                         ├── pyproject.toml
                                                                         ├── requirements.txt
                                                                         └── .env.example
```

### Pipeline Stages (with logging)

Every stage emits structured, timestamped logs so you can see exactly what happens:

1. **Ingestion** — Fetches the spec from a Swagger URL or reads a local file. Parses OpenAPI 3.x / Swagger 2.x / Postman v2.1 into a canonical `APISpec` model.
2. **Capability Mining** — Groups endpoints by tag/resource, clusters similar GET endpoints into unified search tools, generates snake_case names.
3. **AI Reasoning** *(optional, `--use-k2`)* — Sends tools to K2 (MBZUAI IFM) or Dedalus API for enhancement. The AI improves names, descriptions, param docs, and safety classification. Falls back gracefully if a provider is unreachable.
4. **Safety Classification** — Classifies each tool as read/write/destructive using HTTP method + keyword analysis. Applies allowlist/denylist, blocks destructive tools, redacts PII fields, adds safety badges.
5. **Code Generation** — Produces a complete Python MCP server (using `dedalus_mcp`), plus tests, deployment files (`main.py`, `pyproject.toml`), and environment config.

---

## Quick Start

```bash
pip install -r requirements.txt
```

### From a Swagger URL (recommended)

```bash
# Start your API (example: our test math app)
python test_application/app.py  # serves Swagger at http://127.0.0.1:8001/docs

# Generate MCP server from the live Swagger endpoint
python -m mcp_adapter generate \
  --url http://127.0.0.1:8001/openapi.json \
  --output output/math-api-mcp \
  --name math-api

# With AI-enhanced schemas
python -m mcp_adapter generate \
  --url http://127.0.0.1:8001/openapi.json \
  --output output/math-api-mcp \
  --name math-api \
  --use-k2
```

### From a local file

```bash
python -m mcp_adapter generate \
  --spec examples/petstore.yaml \
  --output output/petstore-mcp
```

### Run the generated server

```bash
cd output/math-api-mcp
pip install -r requirements.txt
cp .env.example .env   # fill in your API key
python server.py       # starts on http://127.0.0.1:8000/mcp
```

---

## CLI Reference

### `generate`

| Option | Description |
|--------|-------------|
| `--spec PATH` | Path to local API spec file (OpenAPI YAML/JSON or Postman) |
| `--url URL` | URL to fetch OpenAPI/Swagger spec from |
| `--output, -o PATH` | Output directory for generated MCP server **(required)** |
| `--name TEXT` | Server name (defaults to API title) |
| `--use-k2` | Use AI reasoning to enhance schemas (K2 or Dedalus fallback) |
| `--block-destructive` | Block all DELETE/destructive tools |
| `--max-tools INT` | Max tools to generate (0 = unlimited) |
| `--allowlist TEXT` | Comma-separated tool names to include |
| `--denylist TEXT` | Comma-separated tool names to exclude |
| `-v, --verbose` | Enable debug-level logging |

### `inspect`

| Option | Description |
|--------|-------------|
| `--spec PATH` | Path to local API spec file |
| `--url URL` | URL to fetch OpenAPI/Swagger spec from |
| `--json-output` | Output as JSON instead of human-readable table |

---

## AI Reasoning (K2 Integration)

When `--use-k2` is enabled, the pipeline sends tool definitions to an AI for enhancement.

### Provider Priority (with automatic fallback)

1. **K2 (MBZUAI IFM)** — `K2_API_KEY` + optional `K2_BASE_URL`, `K2_MODEL`
2. **Dedalus API** — `DEDALUS_API_KEY` (uses `openai/gpt-4o-mini`)

If the first provider is unreachable, it automatically tries the next. If all fail, it falls back to the original tool definitions.

### What AI enhances

- **Tool names** — `addnumbers` → `add_numbers`
- **Descriptions** — Generic → clear, agent-friendly prose
- **Parameter docs** — Fills in missing descriptions
- **Safety classification** — Semantic re-evaluation beyond HTTP method

### Configuration (.env)

```bash
# Required: at least one reasoning provider
K2_API_KEY=IFM-your-key-here
K2_BASE_URL=https://your-k2-endpoint/v1   # optional
K2_MODEL=K2-Chat                           # optional

# Fallback provider
DEDALUS_API_KEY=dsk-your-key-here
```

---

## Environment Setup

Create a `.env` file in the project root:

```bash
DEDALUS_API_KEY=dsk-your-key-here    # For Dedalus MCP deployment + AI reasoning
K2_API_KEY=IFM-your-key-here         # For K2 reasoning (optional)
```

---

## Supported Input Formats

| Format | Status | Notes |
|--------|--------|-------|
| Swagger/OpenAPI URL | ✅ Supported | `--url http://host/openapi.json` |
| OpenAPI 3.x (YAML/JSON) | ✅ Supported | Best coverage — maps directly to tools |
| Swagger 2.x (YAML/JSON) | ✅ Supported | Auto-detected |
| Postman Collection v2.1 | ✅ Supported | Folders become tags |

---

## Safety & Permissions

Every generated tool is auto-classified:

- 🟢 **read** — Safe, no side effects (GET, HEAD)
- 🟡 **write** — Creates or modifies data (POST, PUT, PATCH)
- 🔴 **destructive** — May permanently delete data (DELETE)

Additional safety features:
- **Allowlist/denylist** — Control exactly which tools are exposed
- **PII redaction** — Sensitive fields (password, token, ssn, etc.) are flagged
- **Description badges** — Tools are annotated with `[WRITES DATA]` or `[DESTRUCTIVE]`
- **`--block-destructive`** — One flag to remove all DELETE tools

---

## Generated Output

```
output/<name>/
├── server.py          # Complete MCP server (dedalus_mcp)
├── main.py            # Entry point for Dedalus deployment
├── pyproject.toml     # Dependencies for deployment
├── test_server.py     # Contract tests + schema validation
├── requirements.txt   # Python dependencies
└── .env.example       # Environment variable template
```

---

## Project Structure

```
Dedalus/
├── .env                     # API keys (DEDALUS_API_KEY, K2_API_KEY)
├── requirements.txt         # Project dependencies
├── README.md                # This file
├── mcp_adapter/             # The adapter generator
│   ├── __init__.py
│   ├── __main__.py          # python -m entry point
│   ├── cli.py               # Click CLI (generate, inspect)
│   ├── logger.py            # Structured coloured logging
│   ├── models.py            # Pydantic data models
│   ├── ingest.py            # OpenAPI/Postman/URL parsers
│   ├── mine.py              # Capability mining
│   ├── reasoning.py         # AI reasoning (K2 / Dedalus)
│   ├── safety.py            # Safety classification + policy
│   └── codegen.py           # MCP server code generator
├── test_application/        # Example target app
│   ├── app.py               # Math REST API with Swagger UI
│   └── openapi.yaml         # OpenAPI 3.0 spec
├── examples/
│   └── petstore.yaml        # Petstore OpenAPI example
└── output/                  # Generated MCP servers
```

---

## Guide: Creating an MCP Middleware from Scratch

This is a step-by-step guide to turn any REST API into an MCP server.

### Step 1: Build your target application

Create a standard REST API. Example (`test_application/app.py`):

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def add(request):
    data = await request.json()
    return JSONResponse({"result": data["a"] + data["b"]})

app = Starlette(routes=[Route("/add", add, methods=["POST"])])
```

### Step 2: Add an OpenAPI spec

Either write one manually (`openapi.yaml`) or serve it from your app:

```python
async def openapi_json(request):
    spec = yaml.safe_load(open("openapi.yaml"))
    return JSONResponse(spec)

# Add route: Route("/openapi.json", openapi_json)
```

### Step 3: Add Swagger UI (optional but recommended)

Serve Swagger UI at `/docs` so you can browse and test your API:

```python
async def swagger_ui(request):
    html = """<html><body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>SwaggerUIBundle({url: '/openapi.json', dom_id: '#swagger-ui'})</script>
    </body></html>"""
    return HTMLResponse(html)
```

### Step 4: Generate the MCP server

```bash
# Without AI
python -m mcp_adapter generate \
  --url http://127.0.0.1:8001/openapi.json \
  --output output/my-api-mcp

# With AI-enhanced schemas
python -m mcp_adapter generate \
  --url http://127.0.0.1:8001/openapi.json \
  --output output/my-api-mcp \
  --use-k2
```

### Step 5: Test the generated server

```bash
cd output/my-api-mcp
cp .env.example .env
python server.py                    # starts MCP server on :8000
python test_server.py               # runs auto-generated tests
```

### Step 6: Test with a Dedalus AI agent

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

client = AsyncDedalus()
runner = DedalusRunner(client)
result = await runner.run(
    input="What is 42 + 58?",
    model="openai/gpt-4o-mini",
    mcp_servers=["http://your-deployed-server/mcp"],
)
```

### Step 7: Deploy via Dedalus

1. Go to [dedaluslabs.ai/dashboard](https://www.dedaluslabs.ai/dashboard/servers)
2. Click **Add Server** → connect your repo
3. Point to the `output/my-api-mcp/` directory (has `main.py` + `pyproject.toml`)
4. Set environment variables (`DEDALUS_API_KEY`, upstream API keys)
5. Deploy

### What happens under the hood

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│ AI Agent │────▶│ MCP Server   │────▶│ Your REST    │────▶│ Database │
│ (Claude, │     │ (generated)  │     │ API          │     │ / Service│
│  GPT, …) │◀────│ dedalus_mcp  │◀────│              │◀────│          │
└──────────┘     └──────────────┘     └──────────────┘     └──────────┘
    MCP               HTTP                 HTTP
    protocol          proxy                your logic
```

The generated MCP server acts as a **middleware**: it receives MCP tool calls from AI agents, translates them into HTTP requests to your API, and returns structured JSON responses.

---

## Roadmap

- [ ] SDK introspection (TypeScript / Python client libs → tools)
- [ ] CLI help scraping (`--help` output → tools)
- [ ] Docs URL scraping (HTML API docs → tools)
- [ ] OAuth2 flow support in generated servers
- [ ] Multi-tenant deployment with per-user token vaults
- [ ] Upstream change detection (re-generate on new API versions)
- [ ] TypeScript server generation (in addition to Python)
