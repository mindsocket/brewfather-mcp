import asyncio
import logging

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
from mcp.types import TextContent

from brewfather_mcp.api import BrewfatherInventoryClient
from brewfather_mcp.inventory import (
    get_fermentables_summary,
    get_hops_summary,
    get_yeast_summary,
    get_miscs_summary, # Assuming you will create this in inventory.py
)
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

brewfather_client = BrewfatherInventoryClient()


@mcp.prompt(
    name="Possible beer styles based on inventory",
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
        text="""What are the styles I can brew with my Brewfather inventary?
        Don't be limit to the items in the inventory, but try to use as much as possible from the inventory.
        Use styles from the latest BJCP.
        """,
    )

    return [assistant, Message(content, role=role)]


@mcp.resource(
    uri="inventory://categories",
    name="Inventory Categories",
    description="Lists the available inventory categories.",
)
async def inventory_categories() -> str:
    content = """
    Fermentables (Grains, Adjuncts, etc..)
    Hops
    Yeasts
    """

    return content


@mcp.resource(
    uri="inventory://fermentables",
    name="Fermentables",
    description="List all the fermentables (malts, adjuncts, grains, etc) inventory.",
)
async def read_fermentables() -> str:
    try:
        data = await brewfather_client.get_fermentables_list()

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


@mcp.resource(
    uri="inventory://fermentables/{identifier}",
    name="Fermentable detail",
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


@mcp.resource(uri="inventory://hops")
async def read_hops() -> str:
    logger.info("received request")

    try:
        data = await brewfather_client.get_hops_list()

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


@mcp.resource(uri="inventory://hops/{identifier}")
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


@mcp.resource(uri="inventory://yeasts")
async def read_yeasts() -> str:
    logger.info("received request")

    try:
        data = await brewfather_client.get_yeasts_list()

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


@mcp.resource(uri="inventory://yeasts/{identifier}")
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
Timestamp: {item.timestamp.seconds}
Created: {item.created.seconds}
Version: {item.version}
ID: {item.id}
Rev: {item.rev}
"""
        return formatted

    except Exception:
        logger.exception("Error happened")
        raise


@mcp.tool()
@mcp.resource(
    uri="inventory://overview",
    name="Brewfather Inventory Overview",
    description="Overview of all the inventory(malts, grains, hops and yeasts). Contains the same data as the PDF/Print export from the app.",
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
@mcp.resource(
    uri="brewfather://batches",
    name="List Batches",
    description="Lists all brew batches.",
)
async def read_batches_list() -> str:
    logger.info("received request for batches list")
    try:
        data = await brewfather_client.get_batches_list()
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
Batch Number: {item.batch_number or 'N/A'}
Status: {item.status or 'N/A'}
Brewer: {item.brewer or 'N/A'}
Brew Date: {brew_date_str}
Recipe Name: {item.recipe_name or 'N/A'}
"""
            formatted_response.append(formatted)
        return "---\n".join(formatted_response) if formatted_response else "No batches found."
    except Exception:
        logger.exception("Error happened while fetching batches list")
        raise


@mcp.resource(
    uri="brewfather://batches/{batch_id}",
    name="Batch Detail",
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
        # This is a simplified representation; a full Batch model would have many more fields.
        # Refer to Brewfather API docs for all available fields if needed.
        formatted_response = f"""ID: {item.id}
Name: {item.name}
Batch Number: {item.batch_number or 'N/A'}
Status: {item.status or 'N/A'}
Brewer: {item.brewer or 'N/A'}
Brew Date: {brew_date_str}
Recipe Name: {item.recipe_name or 'N/A'}
"""
        # Add more fields as necessary from the item object
        return formatted_response
    except Exception:
        logger.exception(f"Error happened while fetching batch detail for {batch_id}")
        raise


@mcp.tool(
    name="Update Batch",
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
@mcp.resource(
    uri="brewfather://recipes",
    name="List Recipes",
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
Style: {item.style_name or 'N/A'}
Type: {item.type or 'N/A'}
"""
            formatted_response.append(formatted)
        return "---\n".join(formatted_response) if formatted_response else "No recipes found."
    except Exception:
        logger.exception("Error happened while fetching recipes list")
        raise


@mcp.resource(
    uri="brewfather://recipes/{recipe_id}",
    name="Recipe Detail",
    description="Get detailed information for a specific recipe.",
)
async def read_recipe_detail(recipe_id: str) -> str:
    logger.info(f"received request for recipe detail: {recipe_id}")
    try:
        # Assuming Recipe model in types.py might be simple.
        # For full details, the Recipe model would need to be comprehensive.
        item = await brewfather_client.get_recipe_detail(recipe_id)
        formatted_response = f"""ID: {item.id}
Name: {item.name}
Author: {item.author or 'N/A'}
Style: {item.style_name or 'N/A'}
Type: {item.type or 'N/A'}
"""
        # Add more fields as necessary from the item object
        # e.g., item.notes, item.data.mash.name, etc.
        # This requires RecipeDetail model to be defined in types.py and used in api.py
        return formatted_response
    except Exception:
        logger.exception(f"Error happened while fetching recipe detail for {recipe_id}")
        raise


# Miscellaneous Inventory Endpoints
@mcp.resource(
    uri="inventory://miscs",
    name="Miscellaneous Inventory",
    description="Lists all miscellaneous inventory items.",
)
async def read_miscs_list() -> str:
    logger.info("received request for miscellaneous inventory list")
    try:
        data = await brewfather_client.get_miscs_list()
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


@mcp.resource(
    uri="inventory://miscs/{item_id}",
    name="Miscellaneous Item Detail",
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
    name="Update Fermentable Inventory",
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
    name="Update Hop Inventory",
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
    name="Update Miscellaneous Inventory",
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
    name="Update Yeast Inventory",
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
