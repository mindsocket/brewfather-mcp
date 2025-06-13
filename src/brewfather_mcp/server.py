import asyncio
import logging

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
from mcp.types import TextContent

from brewfather_mcp.api import BrewfatherClient, ListQueryParams
from brewfather_mcp.inventory import (
    get_fermentables_summary,
    get_hops_summary,
    get_yeast_summary,
    get_miscs_summary,
)
from brewfather_mcp.formatter import format_recipe_details
from typing import Optional
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/application.log",  # Path to log file
    filemode="a",
)

logger = logging.getLogger(__name__)

mcp = FastMCP("BrewfatherMCP")

_ = load_dotenv()

brewfather_client = BrewfatherClient()


@mcp.prompt(
    name="suggest_beer_styles",
    description="Ask to list all the possible BJCP styles based on the inventory.",
)
async def styles_based_inventory_prompt() -> list[Message]:
    assistant = Message(
        content=TextContent(
            type="text",
            text="""You are an experienced homebrewer with deep knowledge of the brewing process at homebrewer level, ingredients and styles.
            You are not focused on give a full recipe, just an overview of what styles are possible based on ingredients we already have in the inventory and by acquiring extra ingredients.
            Try to optimize the usage of the ingredients on inventory but  don't go out of the style, suggest acquiring new ingredients to stay inside the style guidelines.
            """,
        ),
        role="assistant",
    )
    role = "user"
    content = TextContent(
        type="text",
        text="""What are the styles I can brew with my Brewfather inventory?
        Don't be limit to the items in the inventory, but try to use as much as possible from the inventory.
        Use styles from the latest BJCP.
        """,
    )

    return [assistant, Message(content, role=role)]


@mcp.tool(
    name="list_inventory_categories",
    description="Lists the available inventory categories.",
)
async def inventory_categories() -> str:
    content = """
    Fermentables (Grains, Adjuncts, etc..)
    Hops
    Yeasts
    """

    return content

@mcp.tool(
    name="list_fermentables",
    description="List all the fermentables (malts, adjuncts, grains, etc) inventory.",
)
async def read_fermentables() -> str:
    try:
        params = ListQueryParams()
        params.inventory_exists = True
        params.limit = 50
        data = await brewfather_client.get_fermentables_list(params)

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""Name: {item.name}
Type: {item.type}
Supplier: {item.supplier}
Quantity: {item.inventory} kg
Identifier: {item.id}
"""

            formatted_response.append(formatted)

        return "---\n".join(formatted_response)
    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool(
    name="get_fermentable_detail",
    description="Detailed information of the fermentable item.",
)
async def read_fermentable_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_fermentable_detail(identifier)

        formatted_response = f"""Name: {item.name}
Type: {item.type}
Supplier: {item.supplier}
Inventory: {item.inventory}
Origin: {item.origin}
Grain Category: {item.grain_category}
Potential: {item.potential}
Potential Percentage: {item.potential_percentage}
Color: {item.color}
Moisture: {item.moisture}
Protein: {item.protein}
Diastatic Power: {item.diastatic_power}
Friability: {item.friability}
Not Fermentable: {item.not_fermentable}
Max In Batch: {item.max_in_batch}
Coarse Fine Diff: {item.coarse_fine_diff}
Percent Extract Fine-Ground Dry Basis (FGDB): {item.fgdb}
Hidden: {item.hidden}
Notes: {item.notes}
User Notes: {item.user_notes}
Used In: {item.used_in}
Substitutes: {item.substitutes}
Cost Per Amount: {item.cost_per_amount}
Best Before Date: {item.best_before_date}
Manufacturing Date: {item.manufacturing_date}
Free Amino Nitrogen (FAN): {item.fan}
Percent Coarse-Ground Dry Basic (CGDB): {item.cgdb}
Acid: {item.acid}
ID: {item.id}
"""

        return formatted_response

    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool(
    name="list_hops",
    description="Lists all hops in inventory with their basic properties like alpha acids, quantity, and usage type.",
)
async def read_hops() -> str:
    logger.info("received request")

    try:
        params = ListQueryParams()
        params.inventory_exists = True
        params.limit = 50
        data = await brewfather_client.get_hops_list(params)

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""Identifier: {item.id}
Alpha Acids (A.A): {item.alpha}
Quantity: {item.inventory} grams
Name: {item.name}
Type: {item.type}
Use: {item.use}
"""

            formatted_response.append(formatted)

        return "---\n".join(formatted_response)
    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool(
    name="get_hop_detail",
    description="Detailed information about a specific hop including origin, characteristics, oil composition, and storage details.",
)
async def read_hops_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_hop_detail(identifier)

        formatted = f"""Name: {item.name}
Type: {item.type}
Origin: {item.origin}
Use: {item.use}
Usage: {item.usage}
Alpha Acid (% A.A): {item.alpha}
Beta: {item.beta}
Inventory: {item.inventory}
Time: {item.time}
IBU: {item.ibu}
Oil: {item.oil}
Myrcene: {item.myrcene}
Caryophyllene: {item.caryophyllene}
Humulene: {item.humulene}
Cohumulone: {item.cohumulone}
Farnesene: {item.farnesene}
HSI: {item.hsi}
Year: {item.year}
Temp: {item.temp}
Amount: {item.amount}
Substitutes: {item.substitutes}
Used In: {item.used_in}
Notes: {item.notes}
User Notes: {item.user_notes}
Hidden: {item.hidden}
Best Before Date: {item.best_before_date}
Manufacturing Date: {item.manufacturing_date}
Version: {item.version}
ID: {item.id}
"""
        return formatted

    except:
        logger.exception("Error happened")
        raise


@mcp.tool(
    name="list_yeasts",
    description="Lists all yeasts in inventory with their basic properties like attenuation, quantity, and type.",
)
async def read_yeasts() -> str:
    logger.info("received request")

    try:
        params = ListQueryParams()
        params.inventory_exists = True
        params.limit = 50
        data = await brewfather_client.get_yeasts_list(params)

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""Identifier: {item.id}
Attenuation (%): {item.attenuation}
Quantity: {item.inventory} packets
Name: {item.name}
Type: {item.type}
"""

            formatted_response.append(formatted)

        return "---\n".join(formatted_response)
    except:
        logger.exception("Error happened")
        raise


@mcp.tool(
    name="get_yeast_detail",
    description="Detailed information about a specific yeast including manufacturer, specifications, temperature range, and storage details.",
)
async def read_yeasts_detail(identifier: str) -> str:
    logger.info("received request")

    try:
        item = await brewfather_client.get_yeast_detail(identifier)

        formatted = f"""Name: {item.name}
Type: {item.type}
Form: {item.form}
Laboratory: {item.laboratory}
Product ID: {item.product_id}
Inventory: {item.inventory}
Amount: {item.amount}
Unit: {item.unit}
Attenuation: {item.attenuation}
Min Attenuation: {item.min_attenuation}
Max Attenuation: {item.max_attenuation}
Flocculation: {item.flocculation}
Min Temp: {item.min_temp}
Max Temp: {item.max_temp}
Max ABV: {item.max_abv}
Cells Per Package: {item.cells_per_pkg}
Age Rate: {item.age_rate}
Ferments All: {item.ferments_all}
Description: {item.description}
User Notes: {item.user_notes}
Hidden: {item.hidden}
Best Before Date: {item.best_before_date}
Manufacturing Date: {item.manufacturing_date}
Timestamp: {item.timestamp.seconds if item.timestamp else 'N/A'}
Created: {item.created.seconds if item.created else 'N/A'}
Version: {item.version}
ID: {item.id}
Rev: {item.rev}
"""
        return formatted

    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool(
    name="inventory_summary",
    description="Creates a comprehensive overview of all inventory items including fermentables, hops, yeasts and miscellaneous items.",
)
async def inventory_summary() -> str:
    try:
        ctx = mcp.get_context()
        fermentables_coro = get_fermentables_summary(brewfather_client)
        hops_coro = get_hops_summary(brewfather_client)
        yeasts_coro = get_yeast_summary(brewfather_client)

        result = await asyncio.gather(fermentables_coro, hops_coro, yeasts_coro)
        await ctx.info("API data gathered")

        fermentables, hops, yeasts = result

        response = "Fermentables:\n\n"
        for fermentable in fermentables:
            for k, v in fermentable.items():
                response += f"{k}: {v}\n"
            response += "\n"

        response += "\n---\n"

        response += "Hops:\n\n"
        for hop in hops:
            for k, v in hop.items():
                response += f"{k}: {v}\n"

        response += "\n---\n"

        response += "Yeasts:\n\n"
        for yeast in yeasts:
            for k, v in yeast.items():
                response += f"{k}: {v}\n"
            response += "\n"


        await ctx.report_progress(100, 100)
        return response
    except Exception:
        logger.exception("Failed to show inventory summary")
        raise


# Batch Endpoints
@mcp.tool(
    name="list_batches",
    description="Lists all brew batches.",
)
async def read_batches_list() -> str:
    logger.info("received request for batches list")
    try:
        params = ListQueryParams()
        params.limit = 50
        data = await brewfather_client.get_batches_list(params)
        formatted_response: list[str] = []
        for item in data.root:
            brew_date_str = (
                datetime.fromtimestamp(item.brew_date / 1000).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if item.brew_date
                else "N/A"
            )
            formatted = f"""ID: {item.id}
Name: {item.name}
Batch Number: {item.batch_no or 'N/A'}
Status: {item.status or 'N/A'}
Brewer: {item.brewer or 'N/A'}
Brew Date: {brew_date_str}
Recipe Name: {item.recipe.name}
"""
            formatted_response.append(formatted)
        return "---\n".join(formatted_response) if formatted_response else "No batches found."
    except Exception:
        logger.exception("Error happened while fetching batches list")
        raise


@mcp.tool(
    name="get_batch_detail",
    description="Get detailed information for a specific batch.",
)
async def read_batch_detail(batch_id: str) -> str:
    logger.info(f"received request for batch detail: {batch_id}")
    try:
        item = await brewfather_client.get_batch_detail(batch_id)
        brew_date_str = (
            datetime.fromtimestamp(item.brew_date / 1000).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if item.brew_date
            else "N/A"
        )
        # Format dates
        fermentation_start_str = (
            item.fermentation_start_date.strftime("%Y-%m-%d %H:%M:%S")
            if item.fermentation_start_date
            else "N/A"
        )
        fermentation_end_str = (
            item.fermentation_end_date.strftime("%Y-%m-%d %H:%M:%S")
            if item.fermentation_end_date
            else "N/A"
        )
        bottling_date_str = (
            item.bottling_date.strftime("%Y-%m-%d %H:%M:%S")
            if item.bottling_date
            else "N/A"
        )
        
        formatted_response = f"""Batch Details:
==============
ID: {item.id}
Name: {item.name}
Batch Number: {item.batch_no or 'N/A'}
Status: {item.status or 'N/A'}
Brewer: {item.brewer or 'N/A'}
Brewed: {'Yes' if item.brewed else 'No'}

Recipe Information:
------------------
Recipe Name: {item.recipe.name if item.recipe else 'N/A'}
Recipe ID: {item.recipe_id or 'N/A'}

Schedule:
---------
Brew Date: {brew_date_str}
Fermentation Start: {fermentation_start_str}
Fermentation End: {fermentation_end_str}
Bottling Date: {bottling_date_str}

Gravity & Alcohol:
-----------------
Original Gravity (OG): {item.og or 'N/A'}
Final Gravity (FG): {item.fg or 'N/A'}
ABV: {item.abv or 'N/A'}%

Carbonation:
-----------
Type: {item.carbonation_type or 'N/A'}
Level: {item.carbonation_level or 'N/A'} volumes

Tags: {', '.join(item.tags) if item.tags else 'None'}
"""
        
        if item.notes:
            formatted_response += "\nNotes:\n"
            for note in item.notes:
                note_time = datetime.fromtimestamp(note.timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
                formatted_response += f"- [{note.type}] {note.note} ({note_time})\n"
        
        if item.measurements:
            formatted_response += "\nMeasurements:\n-------------\n"
            for measurement in item.measurements:
                meas_time = measurement.time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(measurement, 'time') and measurement.time else "N/A"
                comment = f" ({measurement.comment})" if hasattr(measurement, 'comment') and measurement.comment else ""
                formatted_response += f"- {measurement.type}: {measurement.value} {measurement.unit} [{meas_time}]{comment}\n"
        
        if item.measurement_devices:
            formatted_response += "\nMeasurement Devices:\n------------------\n"
            for device in item.measurement_devices:
                device_name = device.get('name', 'Unknown Device')
                device_type = device.get('type', 'N/A')
                formatted_response += f"- {device_name} ({device_type})\n"
        
        # Add recipe details if available
        if item.recipe:
            formatted_response += "\n\n" + "="*50 + "\n"
            formatted_response += "RECIPE DETAILS\n"
            formatted_response += "="*50 + "\n\n"
            formatted_response += format_recipe_details(item.recipe)
        
        # Add batch metadata
        formatted_response += "\n\nBatch Metadata:\n--------------\n"
        formatted_response += f"Batch ID: {item.id}\n"
        
        return formatted_response
    except Exception:
        logger.exception(f"Error happened while fetching batch detail for {batch_id}")
        raise


@mcp.tool(
    name="update_batch",
    description="Updates a batch's status or measured values.",
)
async def update_batch(
    batch_id: str,
    status: Optional[str] = None,
    measuredMashPh: Optional[float] = None,
    measuredBoilSize: Optional[float] = None,
    measuredFirstWortGravity: Optional[float] = None,
    measuredPreBoilGravity: Optional[float] = None,
    measuredPostBoilGravity: Optional[float] = None,
    measuredKettleSize: Optional[float] = None,
    measuredOg: Optional[float] = None,
    measuredFermenterTopUp: Optional[float] = None,
    measuredBatchSize: Optional[float] = None,
    measuredFg: Optional[float] = None,
    measuredBottlingSize: Optional[float] = None,
    carbonationTemp: Optional[float] = None,
) -> str:
    logger.info(f"received request to update batch: {batch_id}")
    update_data = {}
    if status:
        update_data["status"] = status
    if measuredMashPh is not None:
        update_data["measuredMashPh"] = measuredMashPh
    if measuredBoilSize is not None:
        update_data["measuredBoilSize"] = measuredBoilSize
    if measuredFirstWortGravity is not None:
        update_data["measuredFirstWortGravity"] = measuredFirstWortGravity
    if measuredPreBoilGravity is not None:
        update_data["measuredPreBoilGravity"] = measuredPreBoilGravity
    if measuredPostBoilGravity is not None:
        update_data["measuredPostBoilGravity"] = measuredPostBoilGravity
    if measuredKettleSize is not None:
        update_data["measuredKettleSize"] = measuredKettleSize
    if measuredOg is not None:
        update_data["measuredOg"] = measuredOg
    if measuredFermenterTopUp is not None:
        update_data["measuredFermenterTopUp"] = measuredFermenterTopUp
    if measuredBatchSize is not None:
        update_data["measuredBatchSize"] = measuredBatchSize
    if measuredFg is not None:
        update_data["measuredFg"] = measuredFg
    if measuredBottlingSize is not None:
        update_data["measuredBottlingSize"] = measuredBottlingSize
    if carbonationTemp is not None:
        update_data["carbonationTemp"] = carbonationTemp

    if not update_data:
        return "No update parameters provided."

    try:
        await brewfather_client.update_batch_detail(batch_id, update_data)
        return f"Batch {batch_id} updated successfully."
    except Exception:
        logger.exception(f"Error happened while updating batch {batch_id}")
        raise


# Recipe Endpoints
@mcp.tool(
    name="list_recipes",
    description="Lists all recipes.",
)
async def read_recipes_list() -> str:
    logger.info("received request for recipes list")
    try:
        data = await brewfather_client.get_recipes_list()
        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""ID: {item.id}
Name: {item.name}
Author: {item.author or 'N/A'}
Style: {item.style.name if item.style else 'N/A'}
Type: {item.type or 'N/A'}
"""
            formatted_response.append(formatted)
        return "---\n".join(formatted_response) if formatted_response else "No recipes found."
    except Exception:
        logger.exception("Error happened while fetching recipes list")
        raise


@mcp.tool(
    name="get_recipe_detail",
    description="Get detailed information for a specific recipe including ingredients, process details and specifications.",
)
async def read_recipe_detail(recipe_id: str) -> str:
    logger.info(f"received request for recipe detail: {recipe_id}")
    try:
        item = await brewfather_client.get_recipe_detail(recipe_id)
        return format_recipe_details(item)
    except Exception:
        logger.exception(f"Error happened while fetching recipe detail for {recipe_id}")
        raise


# Miscellaneous Inventory Endpoints
@mcp.tool(
    name="list_misc_items",
    description="Lists all miscellaneous inventory items.",
)
async def read_miscs_list() -> str:
    logger.info("received request for miscellaneous inventory list")
    try:
        params = ListQueryParams()
        params.inventory_exists = True
        params.limit = 50
        data = await brewfather_client.get_miscs_list(params)

        formatted_response: list[str] = []
        for item in data.root:
            formatted = f"""ID: {item.id}
Name: {item.name}
Type: {item.type or 'N/A'}
Inventory: {item.inventory} units (actual unit depends on item)
Notes: {item.notes or 'N/A'}
"""
            formatted_response.append(formatted)
        return "---\n".join(formatted_response) if formatted_response else "No miscellaneous items found."
    except Exception:
        logger.exception("Error happened while fetching miscellaneous inventory list")
        raise


@mcp.tool(
    name="get_misc_detail",
    description="Get detailed information for a specific miscellaneous inventory item.",
)
async def read_misc_detail(item_id: str) -> str:
    logger.info(f"received request for miscellaneous item detail: {item_id}")
    try:
        # Assuming Miscellaneous model in types.py might be simple for list view.
        # For full details, a MiscellaneousDetail model would be needed.
        item = await brewfather_client.get_misc_detail(item_id)
        formatted_response = f"""ID: {item.id}
Name: {item.name}
Type: {item.type or 'N/A'}
Inventory: {item.inventory} units
Notes: {item.notes or 'N/A'}
"""
        # Add more fields if a more detailed model (e.g., MiscellaneousDetail) is implemented
        return formatted_response
    except Exception:
        logger.exception(f"Error happened while fetching miscellaneous item detail for {item_id}")
        raise


# Inventory Update Tools
@mcp.tool(
    name="update_fermentable_inventory",
    description="Sets the inventory amount for a specific fermentable.",
)
async def update_fermentable_inventory_tool(item_id: str, inventory_amount: float) -> str:
    logger.info(f"Tool: update_fermentable_inventory_tool called for item {item_id} with amount {inventory_amount}")
    try:
        await brewfather_client.update_fermentable_inventory(item_id, inventory_amount)
        return f"Fermentable inventory for item {item_id} updated to {inventory_amount} kg."
    except Exception:
        logger.exception(f"Error updating fermentable inventory for item {item_id}")
        raise


@mcp.tool(
    name="update_hop_inventory",
    description="Sets the inventory amount for a specific hop.",
)
async def update_hop_inventory_tool(item_id: str, inventory_amount: float) -> str:
    logger.info(f"Tool: update_hop_inventory_tool called for item {item_id} with amount {inventory_amount}")
    try:
        await brewfather_client.update_hop_inventory(item_id, inventory_amount)
        return f"Hop inventory for item {item_id} updated to {inventory_amount} grams."
    except Exception:
        logger.exception(f"Error updating hop inventory for item {item_id}")
        raise


@mcp.tool(
    name="update_misc_inventory",
    description="Sets the inventory amount for a specific miscellaneous item.",
)
async def update_misc_inventory_tool(item_id: str, inventory_amount: float) -> str:
    logger.info(f"Tool: update_misc_inventory_tool called for item {item_id} with amount {inventory_amount}")
    try:
        await brewfather_client.update_misc_inventory(item_id, inventory_amount)
        return f"Miscellaneous inventory for item {item_id} updated to {inventory_amount} units."
    except Exception:
        logger.exception(f"Error updating miscellaneous inventory for item {item_id}")
        raise


@mcp.tool(
    name="update_yeast_inventory",
    description="Sets the inventory amount for a specific yeast.",
)
async def update_yeast_inventory_tool(item_id: str, inventory_amount: float) -> str:
    logger.info(f"Tool: update_yeast_inventory_tool called for item {item_id} with amount {inventory_amount}")
    try:
        await brewfather_client.update_yeast_inventory(item_id, inventory_amount)
        return f"Yeast inventory for item {item_id} updated to {inventory_amount} packets."
    except Exception:
        logger.exception(f"Error updating yeast inventory for item {item_id}")
        raise
