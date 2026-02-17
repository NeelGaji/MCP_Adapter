# MYME — Make Your MCP Easy

Youtube tutorial: [Youtube Tutorial](https://youtu.be/6wxYa0HstmA)
Devpost - https://devpost.com/software/myme-make-your-mcp-easy

**One command** to turn any Swagger/OpenAPI URL into a deployed MCP server.

```bash
python -m mcp_adapter generate --url https://your-api.com/openapi.json -o output/my-mcp --name my-api
```

No templates, no scaffolding — purely generative. Code is validated with `ast.parse()` and auto-repaired if needed.

---

## Hackathon Sponsors & Pipeline Integration

MYME is built on top of an incredible stack of sponsor technologies. Each stage of the pipeline is powered by a different sponsor:

```
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────┐
  │  1. DESIGN   │──▶│  2. INGEST   │──▶│  3. DISCOVER  │──▶│  4. GENERATE │──▶│  5. TEST     │──▶│  6. DEPLOY  │
  │              │   │              │   │              │   │              │   │              │   │            │
  │  Figma MCP   │   │ Gemini 2.5   │   │ Featherless  │   │ Featherless  │   │ Featherless  │   │ Dedalus    │
  │  (UI Design) │   │ Flash        │   │ DeepSeek R1  │   │ DeepSeek V3  │   │ DeepSeek V3  │   │ MCP + Auth │
  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘   └────────────┘
        │                  │                  │                   │                  │                  │
    Figma MCP          Google AI         Featherless AI      Featherless AI     Featherless AI     Dedalus Labs
```

### Sponsor → Pipeline Mapping

| Pipeline Stage | Sponsor | Technology | What It Does |
|---|---|---|---|
| **UI Design** | [Figma MCP](https://www.figma.com/) | Figma MCP Server | The entire MYME frontend UI was planned and designed using the Figma MCP |
| **Ingest** | [Google AI](https://ai.google.dev/) | Gemini 2.5 Flash | Parses and understands unstructured API documentation and raw docs |
| **Discover & Mine** | [Featherless AI](https://featherless.ai/) | DeepSeek R1 (Reasoning) | Deep reasoning to group endpoints into high-level MCP tools, classify capabilities, and resolve edge cases |
| **Schema Generation** | [Dedalus Labs](https://www.dedaluslabs.ai/) | Dedalus API | Synthesizes clean type schemas for tool inputs and outputs |
| **Code Generation** | [Featherless AI](https://featherless.ai/) | DeepSeek V3 | Generates the complete MCP server code (`server.py`) in a single LLM call — purely generative |
| **Test Generation** | [Featherless AI](https://featherless.ai/) | DeepSeek V3 | Generates contract test suites to validate every tool in the MCP server |
| **Deploy** | [Dedalus Labs](https://www.dedaluslabs.ai/) | Dedalus MCP + Auth | Deploys the generated MCP server to production. For authenticated APIs, Dedalus MCP Auth handles credential management |
| **Billing & Credits** | [Flowglad](https://flowglad.com/) | Flowglad Payments | Integrated payment system — test mode payments to purchase credits that power MYME's generation pipeline |

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

1. **Ingest** — Fetches the spec from a URL or local file. Parses OpenAPI 3.x / Swagger 2.x / Postman v2.1 using **Gemini 2.5 Flash**.
2. **Mine** — Groups endpoints into high-level tools using **DeepSeek R1** reasoning via Featherless AI.
3. **Safety** — Classifies tools as read/write/destructive. Adds safety badges. Applies allowlist/denylist.
4. **Codegen** — **DeepSeek V3** (via Featherless AI) generates the complete `server.py` in a single LLM call. Validated with `ast.parse()`.
5. **Output** — Writes `server.py`, `test_server.py`, `main.py`, `pyproject.toml`, `.env.example`, `requirements.txt`.
6. **Deploy** — Pushes to GitHub and deploys via **Dedalus MCP**. Authenticated APIs use **Dedalus MCP Auth**.

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

### Step 4: Query your deployed MCP server

Use `query_mcp.py` to talk to any deployed MCP server in natural language:

```bash
# Query by server slug
python query_mcp.py --server your-user/my-api "What is 10 divided by 3?"

# Interactive mode — keep chatting
python query_mcp.py --server your-user/my-api --interactive
```

If the API requires auth and credentials aren't configured, the tool will detect the error and tell you exactly what to set on the Dedalus dashboard.

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

## Querying Deployed MCP Servers — `query_mcp.py`

A standalone CLI to query **any** Dedalus-deployed MCP server in natural language. Works from anywhere — no local files needed.

### Usage

```bash
# Query a deployed server by slug
python query_mcp.py --server user/math-api "What is 10 divided by 3?"

# Interactive chat mode
python query_mcp.py --server user/math-api --interactive

# Use a different model
python query_mcp.py --server user/my-api --model openai/gpt-4o "Describe the API"
```

### Options

| Option | Description |
|--------|-------------|
| `--server, -s` | MCP server slug (e.g. `user/math-api`) — **required** |
| `--model, -m` | AI model (default: `openai/gpt-4o-mini`) |
| `--interactive, -i` | Interactive chat mode |

### How credentials work

If the upstream API requires authentication, the tool **automatically detects auth errors** at runtime (401, 403, etc.) and tells you exactly what to configure:

```
🔒 Authentication required for 'user/petstore-mcp'
   The MCP server returned auth errors:

   ❌ search_pet: {"error": "401 Unauthorized"}

   To fix, configure these env vars on the Dedalus dashboard:
     PETSTORE_MCP_BASE_URL = <your-api-base-url>
     PETSTORE_MCP_API_KEY  = <your-api-key>

   Dashboard: https://www.dedaluslabs.ai/dashboard/servers
   Select 'user/petstore-mcp' → Environment Variables → set the values → Redeploy
```

Credentials are configured on the **Dedalus dashboard** as environment variables — not passed at query time. The `dedalus.json` manifest in the generated output also lists all required env vars for reference

---

## Generated Output

```
output/<name>/
├── server.py          # Complete MCP server — generated by DeepSeek-V3
├── main.py            # Entry point for Dedalus deployment
├── pyproject.toml     # Dependencies for deployment
├── test_server.py     # Auto-generated tests
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── dedalus.json       # Deployment manifest (env vars, auth, tools)
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

## Credit System

MYME uses a credit-based system. Each API tool generated into an MCP server costs **1 credit**. Credits can be purchased at **100 credits for $10.00**.

### Check your balance

```bash
curl http://127.0.0.1:8080/api/credits/sudharshan
```

### Add credits manually (test mode)

To add credits directly via the backend API (no payment required in test mode):

```bash
# Add 100 credits
curl -X POST http://127.0.0.1:8080/api/credits/purchase \
  -H "Content-Type: application/json" \
  -d '{"user": "sudharshan", "credits": 100}'

# Add a custom amount (e.g. 500 credits)
curl -X POST http://127.0.0.1:8080/api/credits/purchase \
  -H "Content-Type: application/json" \
  -d '{"user": "sudharshan", "credits": 500}'
```

You can also click the **Buy** button in the sidebar or on the Generate page — in test mode, credits are added instantly without payment.

### Pricing info

```bash
curl http://127.0.0.1:8080/api/credits/pricing
```

### How credits are charged

- **1 credit per tool** generated during the Generate step
- Credits are checked **before** generation starts (HTTP 402 if insufficient)
- Credits are deducted **after** successful generation
- Credit data is stored in `.credits/sudharshan.json`

---

## Project Structure

```
Dedalus/
├── .env                     # FEATHERLESS_API_KEY (+ optional K2, Dedalus keys)
├── requirements.txt
├── query_mcp.py             # Query any deployed MCP server
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

## Team

- Hardik Amarwani (hardikamarwani@gmail.com)
- Sudharshan Ramesh
- Neel Gajiwala ( ng3373@nyu.edu )
- Harshini Kumar
```
