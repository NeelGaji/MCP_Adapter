# MCP Adapter Generator

**One command** to turn any Swagger/OpenAPI URL into a deployed MCP server.

```bash
python -m mcp_adapter generate --url https://your-api.com/openapi.json -o output/my-mcp --name my-api
```

Code is generated entirely by **DeepSeek-V3** (via [Featherless AI](https://featherless.ai)), validated with `ast.parse()`, and auto-repaired if needed. No templates, no scaffolding — purely generative.

---

## How It Works

```
  Swagger URL              Pipeline                    DeepSeek-V3               Output
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────┐
  │  1. INGEST   │──▶│  2. MINE     │──▶│  3. SAFETY   │──▶│  4. CODEGEN  │──▶│  5. OUTPUT  │
  │              │   │              │   │              │   │  (LLM)       │   │            │
  │ Fetch & parse│   │ Group into   │   │ Classify     │   │ DeepSeek-V3  │   │ server.py  │
  │ OpenAPI spec │   │ tools        │   │ read/write/  │   │ generates    │   │ + tests    │
  │              │   │              │   │ destructive  │   │ full server  │   │ + deploy   │
  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └────────────┘
```

1. **Ingest** — Fetches the spec from a URL or local file. Parses OpenAPI 3.x / Swagger 2.x / Postman v2.1.
2. **Mine** — Groups endpoints into high-level tools, merges related GET endpoints into search tools.
3. **Safety** — Classifies tools as read/write/destructive. Adds safety badges. Applies allowlist/denylist.
4. **Codegen** — DeepSeek-V3 generates the complete `server.py` in a single LLM call. Validated with `ast.parse()`.
5. **Output** — Writes `server.py`, `test_server.py`, `main.py`, `pyproject.toml`, `.env.example`, `requirements.txt`.

---

## Quick Start

### Prerequisites

```bash
pip install -r requirements.txt
```

Add your Featherless API key to `.env`:

```bash
FEATHERLESS_API_KEY=your-featherless-api-key
```

Get a free key at [featherless.ai](https://featherless.ai).

### Single Command — Generate + Deploy

```bash
python -m mcp_adapter generate \
  --url https://your-api.com/openapi.json \
  -o output/my-api-mcp \
  --name my-api \
  --deploy
```

This will:
1. Fetch & parse the OpenAPI spec
2. Generate a complete MCP server via DeepSeek-V3
3. Validate with `ast.parse()`
4. Create a GitHub repo and push the code
5. Open the Dedalus dashboard for one-click deployment

### Generate Only (no deploy)

```bash
python -m mcp_adapter generate \
  --url https://your-api.com/openapi.json \
  -o output/my-api-mcp \
  --name my-api
```

Run locally:

```bash
cd output/my-api-mcp
pip install -r requirements.txt
cp .env.example .env   # fill in your upstream API key
python server.py       # MCP server on http://127.0.0.1:8000/mcp
```

### From a Local File

```bash
python -m mcp_adapter generate \
  --spec examples/petstore.yaml \
  -o output/petstore-mcp
```

---

## CLI Reference

### `generate`

| Option | Description |
|--------|-------------|
| `--url URL` | Swagger/OpenAPI URL to fetch spec from |
| `--spec PATH` | Path to local spec file (OpenAPI YAML/JSON or Postman) |
| `-o, --output PATH` | Output directory **(required)** |
| `--name TEXT` | Server name (defaults to API title) |
| `--use-k2` | AI-enhance tool names and descriptions |
| `--block-destructive` | Remove all DELETE tools |
| `--max-tools INT` | Max tools to generate (0 = unlimited) |
| `--allowlist TEXT` | Only include these tools (comma-separated) |
| `--denylist TEXT` | Exclude these tools (comma-separated) |
| `--deploy` | Push to GitHub + open Dedalus dashboard |
| `--github-org TEXT` | GitHub org for the repo (default: personal account) |
| `-v, --verbose` | Debug logging |

### `inspect`

Preview what tools would be generated without writing files:

```bash
python -m mcp_adapter inspect --url https://your-api.com/openapi.json
python -m mcp_adapter inspect --url https://your-api.com/openapi.json --json-output
```

---

## Environment Setup

Create a `.env` in the project root:

```bash
# Required — powers the code generation
FEATHERLESS_API_KEY=your-featherless-api-key

# Required for --deploy flag
GITHUB_TOKEN=ghp_your-personal-access-token

# Optional — for K2 reasoning (--use-k2 flag)
K2_API_KEY=IFM-your-key-here

# Optional — for Dedalus deployment
DEDALUS_API_KEY=dsk-your-key-here
```

**GitHub Token**: Create at [github.com/settings/tokens](https://github.com/settings/tokens) with `repo` scope.

---

## End-to-End Guide: Swagger URL → Deployed MCP Server

### Step 1: Set up your `.env`

```bash
FEATHERLESS_API_KEY=your-featherless-key    # for code generation
GITHUB_TOKEN=ghp_your-github-token          # for --deploy
DEDALUS_API_KEY=dsk-your-dedalus-key        # for Dedalus platform
```

### Step 2: One command — generate + push to GitHub

```bash
python -m mcp_adapter generate \
  --url https://your-api.com/openapi.json \
  -o output/my-api-mcp \
  --name my-api \
  --deploy
```

This will:
1. Fetch and parse the OpenAPI spec
2. Generate a complete MCP server via DeepSeek-V3
3. Validate with `ast.parse()` (auto-repair if needed)
4. Create a GitHub repo `my-api` and push all files
5. Open the Dedalus dashboard in your browser

To push to a GitHub org instead of your personal account:

```bash
python -m mcp_adapter generate \
  --url https://your-api.com/openapi.json \
  -o output/my-api-mcp \
  --name my-api \
  --deploy --github-org your-org
```

### Step 3: Deploy on Dedalus (one-time per server)

The `--deploy` flag opens the Dedalus dashboard automatically. Then:

1. Click **Add Server** → connect the repo that was just created
2. Set environment variables:
   - `MY_API_BASE_URL` = your upstream API URL
   - `MY_API_API_KEY` = your upstream API key
3. Click **Deploy**

Your MCP server will be live at:
```
https://mcp.dedaluslabs.ai/your-org/my-api/mcp
```

> **Scaling tip**: After the first deploy, subsequent `--deploy` runs to the same repo will push updates and Dedalus will auto-redeploy.

### Step 4: Use from any AI agent

```python
from dedalus_labs import AsyncDedalus, DedalusRunner

client = AsyncDedalus()
runner = DedalusRunner(client)
result = await runner.run(
    input="Find all available dogs",
    model="openai/gpt-4o-mini",
    mcp_servers=["your-org/my-api"],
)
print(result)
```

Or test locally before deploying:

```bash
cd output/my-api-mcp
pip install -r requirements.txt
cp .env.example .env
python server.py              # http://127.0.0.1:8000/mcp
python test_server.py          # auto-generated tests
```

### Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│ AI Agent │────▶│ MCP Server   │────▶│ Your REST    │────▶│ Database │
│ (Claude, │     │ (generated)  │     │ API          │     │ / Service│
│  GPT, …) │◀────│ dedalus_mcp  │◀────│              │◀────│          │
└──────────┘     └──────────────┘     └──────────────┘     └──────────┘
    MCP               HTTP                 HTTP
    protocol          proxy                your logic
```

---

## Generated Output

```
output/<name>/
├── server.py          # Complete MCP server — generated by DeepSeek-V3
├── main.py            # Entry point for Dedalus deployment
├── pyproject.toml     # Dependencies for deployment
├── test_server.py     # Auto-generated tests
├── requirements.txt   # Python dependencies
└── .env.example       # Environment variable template
```

---

## Supported Input Formats

| Format | Notes |
|--------|-------|
| Swagger/OpenAPI URL | `--url http://host/openapi.json` |
| OpenAPI 3.x (YAML/JSON) | Best coverage |
| Swagger 2.x (YAML/JSON) | Auto-detected |
| Postman Collection v2.1 | Folders become tags |

---

## Safety & Permissions

Every tool is auto-classified:

- 🟢 **read** — No side effects (GET)
- 🟡 **write** — Creates or modifies data (POST, PUT, PATCH) → `[WRITES DATA]`
- 🔴 **destructive** — Deletes data (DELETE) → `[DESTRUCTIVE]`

Controls: `--block-destructive`, `--allowlist`, `--denylist`, `--max-tools`

---

## Project Structure

```
Dedalus/
├── .env                     # FEATHERLESS_API_KEY (+ optional K2, Dedalus keys)
├── requirements.txt
├── mcp_adapter/
│   ├── cli.py               # Click CLI
│   ├── ingest.py            # OpenAPI/Postman/URL parser
│   ├── mine.py              # Endpoint → tool grouping
│   ├── safety.py            # Safety classification
│   ├── agentic_codegen.py   # DeepSeek-V3 code generation
│   ├── reasoning.py         # K2 AI reasoning (optional)
│   ├── models.py            # Data models
│   └── logger.py            # Structured logging
├── examples/
│   └── petstore.yaml        # Complex API example
├── test_application/
│   └── app.py               # Simple math API for testing
└── output/                  # Generated MCP servers
```
