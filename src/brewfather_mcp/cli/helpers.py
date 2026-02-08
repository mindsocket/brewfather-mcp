"""CLI helper utilities."""

import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any

import click


def async_command(f: Callable) -> Callable:
    """Decorator to run async click commands with asyncio.run."""
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(f(*args, **kwargs))
    return wrapper


json_option = click.option("--json", "use_json", is_flag=True, default=False, help="Output raw JSON")


def get_client(ctx: click.Context):  # type: ignore[return]
    """Get or create the BrewfatherClient from context (lazy initialization)."""
    if ctx.obj.get("client") is None:
        from brewfather_mcp.api import BrewfatherClient
        from brewfather_mcp.cli.auth import load_credentials
        user_id, api_key = load_credentials()
        ctx.obj["client"] = BrewfatherClient(user_id=user_id, api_key=api_key)
    return ctx.obj["client"]
