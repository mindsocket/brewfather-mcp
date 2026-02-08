"""Recipe CLI subcommands."""

import json

import click

from brewfather_mcp.api import ListQueryParams
from brewfather_mcp.cli.helpers import async_command, get_client, json_option
import brewfather_mcp.tools.recipe as t_recipe


@click.group()
def recipe() -> None:
    """Manage recipes."""


@recipe.command("list")
@click.pass_context
@json_option
@async_command
async def recipe_list(ctx: click.Context, use_json: bool) -> None:
    """List all recipes."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        params = ListQueryParams()
        params.limit = 100
        data = await client.get_recipes_list(params)
        click.echo(json.dumps([item.model_dump() for item in data.root], indent=2, default=str))
    else:
        click.echo(await t_recipe.list_recipes(client))


@recipe.command("detail")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def recipe_detail(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show detailed information for a recipe."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        item = await client.get_recipe_detail(id)
        click.echo(json.dumps(item.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_recipe.get_recipe_detail(client, id))


@recipe.command("enums")
def recipe_enums() -> None:
    """Show valid enum values for recipe creation."""
    click.echo(t_recipe.get_recipe_enums())
