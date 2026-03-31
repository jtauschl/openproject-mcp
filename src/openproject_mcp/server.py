from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP

from .client import OpenProjectClient
from .config import Settings, configure_logging
from .tools import register_tools


@dataclass(slots=True)
class AppContext:
    settings: Settings
    client: OpenProjectClient


@asynccontextmanager
async def app_lifespan(_: FastMCP) -> AsyncIterator[AppContext]:
    settings = Settings.from_env()
    configure_logging(settings.log_level)
    client = OpenProjectClient(settings)
    try:
        yield AppContext(settings=settings, client=client)
    finally:
        await client.aclose()


mcp = FastMCP("OpenProject MCP", json_response=True, lifespan=app_lifespan)
register_tools(mcp)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
