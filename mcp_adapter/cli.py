"""CLI entry point for the MCP Adapter Generator.

Usage:
    python -m mcp_adapter generate --spec path/to/openapi.yaml --output ./output
    python -m mcp_adapter generate --url http://host/openapi.json --output ./output --use-k2
    python -m mcp_adapter inspect  --spec path/to/openapi.yaml
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

load_dotenv()

from .codegen import generate
from .ingest import ingest
from .logger import setup_logging, get_logger
from .mine import mine_tools
from .models import SafetyLevel
from .reasoning import enhance_tools_with_k2
from .safety import SafetyPolicy, apply_safety


@click.group()
@click.version_option(version="0.2.0", prog_name="mcp-adapter")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Verbose logging.")
def cli(verbose: bool):
    """MCP Adapter Generator — turn any API spec into a working MCP server."""
    setup_logging(verbose=verbose)


# ── generate ────────────────────────────────────────────────────────────────


@cli.command("generate")
@click.option(
    "--spec",
    default=None,
    type=click.Path(exists=True),
    help="Path to API spec file (OpenAPI YAML/JSON or Postman collection).",
)
@click.option(
    "--url",
    default=None,
    help="URL to fetch OpenAPI/Swagger spec from (e.g. http://host/openapi.json).",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(),
    help="Output directory for generated MCP server.",
)
@click.option(
    "--name",
    default=None,
    help="Server name (defaults to API title).",
)
@click.option(
    "--use-k2",
    is_flag=True,
    default=False,
    help="Use Kimi K2 AI to enhance tool names, descriptions, and schemas.",
)
@click.option(
    "--block-destructive",
    is_flag=True,
    default=False,
    help="Block all destructive (DELETE) tools.",
)
@click.option(
    "--max-tools",
    default=0,
    type=int,
    help="Max number of tools to generate (0 = no limit).",
)
@click.option(
    "--allowlist",
    default=None,
    help="Comma-separated list of tool names to include (others excluded).",
)
@click.option(
    "--denylist",
    default=None,
    help="Comma-separated list of tool names to exclude.",
)
def generate_cmd(
    spec: str | None,
    url: str | None,
    output: str,
    name: str | None,
    use_k2: bool,
    block_destructive: bool,
    max_tools: int,
    allowlist: str | None,
    denylist: str | None,
):
    """Generate an MCP server from an API specification."""
    logger = get_logger()

    if not spec and not url:
        click.echo("Error: Provide either --spec (file) or --url (Swagger URL).", err=True)
        sys.exit(1)

    source = url if url else spec

    logger.info("=" * 60)
    logger.info("MCP ADAPTER GENERATOR — WORKFLOW START")
    logger.info("=" * 60)
    logger.info("Source: %s", source)
    logger.info("Output: %s", output)
    logger.info("K2 reasoning: %s", "enabled" if use_k2 else "disabled")
    logger.info("")

    # ── Stage 1: Ingestion ────────────────────────────────────────────
    api_spec = ingest(source)
    logger.info(
        "Spec: %s v%s — %d endpoints, %d tags, %d auth schemes",
        api_spec.title, api_spec.version,
        len(api_spec.endpoints), len(api_spec.tags),
        len(api_spec.auth_schemes),
    )

    # ── Stage 2: Capability Mining ────────────────────────────────────
    tools = mine_tools(api_spec)

    # ── Stage 3: K2 Reasoning (optional) ──────────────────────────────
    if use_k2:
        tools = enhance_tools_with_k2(api_spec, tools)

    # ── Stage 4: Safety Classification ────────────────────────────────
    policy = SafetyPolicy(
        block_destructive=block_destructive,
        max_tools=max_tools,
        allowlist=allowlist.split(",") if allowlist else [],
        denylist=denylist.split(",") if denylist else [],
    )
    tools = apply_safety(tools, policy)

    # ── Stage 5: Code Generation ──────────────────────────────────────
    result = generate(api_spec, tools, server_name=name, output_dir=output)

    # ── Summary ───────────────────────────────────────────────────────
    logger.info("")
    logger.info("=" * 60)
    logger.info("WORKFLOW COMPLETE")
    logger.info("=" * 60)
    logger.info("Server: %s (%d tools)", result.server_name, result.tool_count)
    logger.info("Output: %s", result.output_dir)
    logger.info("")
    click.echo(f"\n✅ Done! To run your server:")
    click.echo(f"   cd {output}")
    click.echo(f"   pip install -r requirements.txt")
    click.echo(f"   cp .env.example .env  # fill in your API key")
    click.echo(f"   python server.py")


# ── inspect ─────────────────────────────────────────────────────────────────


@cli.command("inspect")
@click.option(
    "--spec",
    default=None,
    type=click.Path(exists=True),
    help="Path to API spec file.",
)
@click.option(
    "--url",
    default=None,
    help="URL to fetch OpenAPI/Swagger spec from.",
)
@click.option(
    "--json-output",
    is_flag=True,
    default=False,
    help="Output as JSON instead of human-readable.",
)
def inspect_cmd(spec: str | None, url: str | None, json_output: bool):
    """Inspect an API spec and show what tools would be generated."""
    if not spec and not url:
        click.echo("Error: Provide either --spec (file) or --url (Swagger URL).", err=True)
        sys.exit(1)

    source = url if url else spec
    api_spec = ingest(source)
    tools = mine_tools(api_spec)
    tools = apply_safety(tools)

    if json_output:
        data = {
            "api": {
                "title": api_spec.title,
                "version": api_spec.version,
                "base_url": api_spec.base_url,
                "endpoints": len(api_spec.endpoints),
                "tags": api_spec.tags,
            },
            "tools": [
                {
                    "name": t.name,
                    "description": t.description,
                    "safety": t.safety.value,
                    "params": [
                        {
                            "name": p.name,
                            "type": p.json_type,
                            "required": p.required,
                        }
                        for p in t.params
                    ],
                }
                for t in tools
            ],
        }
        click.echo(json.dumps(data, indent=2))
        return

    click.echo(f"API: {api_spec.title} v{api_spec.version}")
    click.echo(f"Base URL: {api_spec.base_url}")
    click.echo(f"Endpoints: {len(api_spec.endpoints)}")
    click.echo(f"Tags: {', '.join(api_spec.tags) or 'none'}")
    click.echo(f"Auth: {', '.join(s.name for s in api_spec.auth_schemes) or 'none'}")
    click.echo("")
    click.echo(f"Tools ({len(tools)}):")
    click.echo("-" * 72)

    for t in tools:
        safety_icon = {"read": "🟢", "write": "🟡", "destructive": "🔴"}[
            t.safety.value
        ]
        params_str = ", ".join(
            f"{p.name}: {p.json_type}{'*' if p.required else '?'}"
            for p in t.params
        )
        click.echo(f"  {safety_icon} {t.name}({params_str})")
        click.echo(f"     {t.description}")


# ── Entry point ─────────────────────────────────────────────────────────────


def main():
    cli()


if __name__ == "__main__":
    main()
