"""Entry point for Dedalus deployment."""

from server import server
import asyncio

if __name__ == "__main__":
    asyncio.run(server.serve())
