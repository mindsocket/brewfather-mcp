"""Brewfather CLI — command-line interface for Brewfather API."""

import click

from brewfather_mcp.cli.auth import auth
from brewfather_mcp.cli.inventory import inventory
from brewfather_mcp.cli.batches import batch
from brewfather_mcp.cli.recipes import recipe


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Brewfather CLI — interact with your Brewfather data from the command line."""
    ctx.ensure_object(dict)
    ctx.obj["json"] = False
    ctx.obj["client"] = None  # Lazy-loaded on first use


cli.add_command(auth)
cli.add_command(inventory)
cli.add_command(batch)
cli.add_command(recipe)
