"""Batch CLI subcommands."""

import json
from typing import Optional

import click

from brewfather_mcp.api import ListQueryParams
from brewfather_mcp.cli.helpers import async_command, get_client, json_option
import brewfather_mcp.tools.batch as t_batch


@click.group()
def batch() -> None:
    """Manage brew batches."""


@batch.command("list")
@click.pass_context
@json_option
@async_command
async def batch_list(ctx: click.Context, use_json: bool) -> None:
    """List all brew batches."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        params = ListQueryParams()
        params.limit = 50
        data = await client.get_batches_list(params)
        click.echo(json.dumps([item.model_dump() for item in data.root], indent=2, default=str))
    else:
        click.echo(await t_batch.list_batches(client))


@batch.command("detail")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def batch_detail(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show detailed information for a batch."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        item = await client.get_batch_detail(id)
        click.echo(json.dumps(item.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_batch.get_batch_detail(client, id))


@batch.command("update")
@click.argument("id")
@click.option("--status", default=None, help="Batch status")
@click.option("--measured-og", type=float, default=None, help="Measured original gravity")
@click.option("--measured-fg", type=float, default=None, help="Measured final gravity")
@click.option("--measured-mash-ph", type=float, default=None, help="Measured mash pH")
@click.option("--measured-boil-size", type=float, default=None, help="Measured boil size (L)")
@click.option("--measured-first-wort-gravity", type=float, default=None, help="Measured first wort gravity")
@click.option("--measured-pre-boil-gravity", type=float, default=None, help="Measured pre-boil gravity")
@click.option("--measured-post-boil-gravity", type=float, default=None, help="Measured post-boil gravity")
@click.option("--measured-kettle-size", type=float, default=None, help="Measured kettle size (L)")
@click.option("--measured-fermenter-top-up", type=float, default=None, help="Measured fermenter top-up (L)")
@click.option("--measured-batch-size", type=float, default=None, help="Measured batch size (L)")
@click.option("--measured-bottling-size", type=float, default=None, help="Measured bottling size (L)")
@click.option("--carbonation-temp", type=float, default=None, help="Carbonation temperature")
@click.pass_context
@async_command
async def batch_update(
    ctx: click.Context,
    id: str,
    status: Optional[str],
    measured_og: Optional[float],
    measured_fg: Optional[float],
    measured_mash_ph: Optional[float],
    measured_boil_size: Optional[float],
    measured_first_wort_gravity: Optional[float],
    measured_pre_boil_gravity: Optional[float],
    measured_post_boil_gravity: Optional[float],
    measured_kettle_size: Optional[float],
    measured_fermenter_top_up: Optional[float],
    measured_batch_size: Optional[float],
    measured_bottling_size: Optional[float],
    carbonation_temp: Optional[float],
) -> None:
    """Update batch status or measured values."""
    client = get_client(ctx)

    update_data: dict = {}
    if status:
        update_data["status"] = status
    if measured_og is not None:
        update_data["measuredOg"] = measured_og
    if measured_fg is not None:
        update_data["measuredFg"] = measured_fg
    if measured_mash_ph is not None:
        update_data["measuredMashPh"] = measured_mash_ph
    if measured_boil_size is not None:
        update_data["measuredBoilSize"] = measured_boil_size
    if measured_first_wort_gravity is not None:
        update_data["measuredFirstWortGravity"] = measured_first_wort_gravity
    if measured_pre_boil_gravity is not None:
        update_data["measuredPreBoilGravity"] = measured_pre_boil_gravity
    if measured_post_boil_gravity is not None:
        update_data["measuredPostBoilGravity"] = measured_post_boil_gravity
    if measured_kettle_size is not None:
        update_data["measuredKettleSize"] = measured_kettle_size
    if measured_fermenter_top_up is not None:
        update_data["measuredFermenterTopUp"] = measured_fermenter_top_up
    if measured_batch_size is not None:
        update_data["measuredBatchSize"] = measured_batch_size
    if measured_bottling_size is not None:
        update_data["measuredBottlingSize"] = measured_bottling_size
    if carbonation_temp is not None:
        update_data["carbonationTemp"] = carbonation_temp

    click.echo(await t_batch.update_batch(client, id, update_data))


@batch.command("brewtracker")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def batch_brewtracker(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show brewing process tracker for a batch."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        tracker = await client.get_batch_brewtracker(id)
        click.echo(json.dumps(tracker.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_batch.get_batch_brewtracker(client, id))


@batch.command("last-reading")
@click.argument("id")
@click.pass_context
@json_option
@async_command
async def batch_last_reading(ctx: click.Context, use_json: bool, id: str) -> None:
    """Show the most recent sensor reading for a batch."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        reading = await client.get_batch_last_reading(id)
        click.echo(json.dumps(reading.model_dump(), indent=2, default=str))
    else:
        click.echo(await t_batch.get_batch_last_reading(client, id))


@batch.command("readings")
@click.argument("id")
@click.option("--limit", default=10, show_default=True, help="Number of recent readings to show")
@click.pass_context
@json_option
@async_command
async def batch_readings(ctx: click.Context, use_json: bool, id: str, limit: int) -> None:
    """Show recent sensor readings for a batch."""
    ctx.obj["json"] = use_json
    client = get_client(ctx)
    if use_json:
        readings = await client.get_batch_readings(id)
        click.echo(json.dumps([r.model_dump() for r in readings.root], indent=2, default=str))
    else:
        click.echo(await t_batch.get_batch_readings_summary(client, id, limit))
