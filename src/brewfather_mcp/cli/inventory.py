"""Inventory CLI subcommands."""

import json

import click

from brewfather_mcp.api import ListQueryParams
from brewfather_mcp.cli.helpers import async_command, get_client, json_option
import brewfather_mcp.tools.fermentable as t_fermentable
import brewfather_mcp.tools.hop as t_hop
import brewfather_mcp.tools.yeast as t_yeast
import brewfather_mcp.tools.misc as t_misc
import brewfather_mcp.tools.inventory as t_inventory


@click.group()
def inventory() -> None:
    """Manage brewing inventory."""


# --- Fermentable subgroup ---

@inventory.group()
def fermentable() -> None:
    """Manage fermentable inventory (malts, grains, adjuncts)."""


@fermentable.command("list")
@click.pass_context
@json_option
@async_command
async def fermentable_list(ctx: click.Context, use_json: bool) -> None:
    """List fermentables with inventory > 0."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        params = ListQueryParams()
        params.limit = 50
        data = await client.get_fermentables_list(params)
        click.echo(json.dumps([item.model_dump() for item in data.root], indent=2, default=str))
    else:
        click.echo(await t_fermentable.list_fermentables(client))


@fermentable.command("detail")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def fermentable_detail(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show full detail for a fermentable."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        item = await client.get_fermentable_detail(id)
        click.echo(json.dumps(item.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_fermentable.get_fermentable_detail(client, id))


@fermentable.command("update")
@click.argument("id")
@click.argument("amount", type=float)
@click.pass_context
@async_command
async def fermentable_update(ctx: click.Context, id: str, amount: float) -> None:
    """Set fermentable inventory amount (kg)."""
    client = get_client(ctx)
    click.echo(await t_fermentable.update_fermentable(client, id, amount))


# --- Hop subgroup ---

@inventory.group()
def hop() -> None:
    """Manage hop inventory."""


@hop.command("list")
@click.pass_context
@json_option
@async_command
async def hop_list(ctx: click.Context, use_json: bool) -> None:
    """List hops with inventory > 0."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        params = ListQueryParams()
        params.limit = 50
        data = await client.get_hops_list(params)
        click.echo(json.dumps([item.model_dump() for item in data.root], indent=2, default=str))
    else:
        click.echo(await t_hop.list_hops(client))


@hop.command("detail")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def hop_detail(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show full detail for a hop."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        item = await client.get_hop_detail(id)
        click.echo(json.dumps(item.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_hop.get_hop_detail(client, id))


@hop.command("update")
@click.argument("id")
@click.argument("amount", type=float)
@click.pass_context
@async_command
async def hop_update(ctx: click.Context, id: str, amount: float) -> None:
    """Set hop inventory amount (grams)."""
    client = get_client(ctx)
    click.echo(await t_hop.update_hop(client, id, amount))


# --- Yeast subgroup ---

@inventory.group()
def yeast() -> None:
    """Manage yeast inventory."""


@yeast.command("list")
@click.pass_context
@json_option
@async_command
async def yeast_list(ctx: click.Context, use_json: bool) -> None:
    """List yeasts with inventory > 0."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        params = ListQueryParams()
        params.limit = 50
        data = await client.get_yeasts_list(params)
        click.echo(json.dumps([item.model_dump() for item in data.root], indent=2, default=str))
    else:
        click.echo(await t_yeast.list_yeasts(client))


@yeast.command("detail")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def yeast_detail(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show full detail for a yeast."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        item = await client.get_yeast_detail(id)
        click.echo(json.dumps(item.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_yeast.get_yeast_detail(client, id))


@yeast.command("update")
@click.argument("id")
@click.argument("amount", type=float)
@click.pass_context
@async_command
async def yeast_update(ctx: click.Context, id: str, amount: float) -> None:
    """Set yeast inventory amount (packets)."""
    client = get_client(ctx)
    click.echo(await t_yeast.update_yeast(client, id, amount))


# --- Misc subgroup ---

@inventory.group()
def misc() -> None:
    """Manage miscellaneous inventory."""


@misc.command("list")
@click.pass_context
@json_option
@async_command
async def misc_list(ctx: click.Context, use_json: bool) -> None:
    """List miscellaneous items with inventory > 0."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        params = ListQueryParams()
        params.limit = 50
        data = await client.get_miscs_list(params)
        click.echo(json.dumps([item.model_dump() for item in data.root], indent=2, default=str))
    else:
        click.echo(await t_misc.list_misc(client))


@misc.command("detail")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def misc_detail(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show full detail for a misc item."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        item = await client.get_misc_detail(id)
        click.echo(json.dumps(item.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_misc.get_misc_detail(client, id))


@misc.command("update")
@click.argument("id")
@click.argument("amount", type=float)
@click.pass_context
@async_command
async def misc_update(ctx: click.Context, id: str, amount: float) -> None:
    """Set misc item inventory amount (units)."""
    client = get_client(ctx)
    click.echo(await t_misc.update_misc(client, id, amount))


# --- Summary ---

@inventory.command()
@click.pass_context
@async_command
async def summary(ctx: click.Context) -> None:
    """Show a combined overview of all inventory."""
    client = get_client(ctx)
    click.echo(await t_inventory.inventory_summary(client))
