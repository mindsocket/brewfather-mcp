"""HTTP/SSE runner for the Brewfather MCP server."""

import asyncio
import logging
from typing import Optional

import click

from brewfather_mcp.server import mcp

logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to")
@click.option("--port", default=8000, help="Port to listen on")
@click.option("--log-level", default="INFO", help="Logging level")
def main(host: str, port: int, log_level: str) -> None:
    """Run the Brewfather MCP server over HTTP/SSE."""
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logger.info(f"Starting Brewfather MCP HTTP server on {host}:{port}")
    
    # Configure server settings
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.settings.log_level = log_level.upper() # type: ignore
    
    # Run the server with SSE transport
    try:
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


def run_http_server(
    host: str = "0.0.0.0", 
    port: int = 8000, 
    log_level: str = "INFO"
) -> None:
    """Programmatic way to run the HTTP server."""
    main(host, port, log_level)


if __name__ == "__main__":
    main()