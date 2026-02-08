import logging
from typing import Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import Message
from mcp.types import TextContent

from brewfather_mcp.api import BrewfatherClient
from brewfather_mcp.types.recipe import RecipeType
from brewfather_mcp.types.hop import HopForm
from brewfather_mcp.types.yeast import YeastType
import brewfather_mcp.tools.fermentable as t_fermentable
import brewfather_mcp.tools.hop as t_hop
import brewfather_mcp.tools.yeast as t_yeast
import brewfather_mcp.tools.misc as t_misc
import brewfather_mcp.tools.batch as t_batch
import brewfather_mcp.tools.recipe as t_recipe
import brewfather_mcp.tools.inventory as t_inventory


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/brewfather_mcp.log",  # Path to log file
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
    return await t_fermentable.list_fermentables(brewfather_client)


@mcp.tool(
    name="get_fermentable_detail",
    description="Detailed information of the fermentable item.",
)
async def read_fermentable_detail(identifier: str) -> str:
    return await t_fermentable.get_fermentable_detail(brewfather_client, identifier)


@mcp.tool(
    name="list_hops",
    description="Lists all hops in inventory with their basic properties like alpha acids, quantity, and usage type.",
)
async def read_hops() -> str:
    return await t_hop.list_hops(brewfather_client)


@mcp.tool(
    name="get_hop_detail",
    description="Detailed information about a specific hop including origin, characteristics, oil composition, and storage details.",
)
async def read_hops_detail(identifier: str) -> str:
    return await t_hop.get_hop_detail(brewfather_client, identifier)


@mcp.tool(
    name="list_yeasts",
    description="Lists all yeasts in inventory with their basic properties like attenuation, quantity, and type.",
)
async def read_yeasts() -> str:
    return await t_yeast.list_yeasts(brewfather_client)


@mcp.tool(
    name="get_yeast_detail",
    description="Detailed information about a specific yeast including manufacturer, specifications, temperature range, and storage details.",
)
async def read_yeasts_detail(identifier: str) -> str:
    return await t_yeast.get_yeast_detail(brewfather_client, identifier)


@mcp.tool(
    name="inventory_summary",
    description="Creates a comprehensive overview of all inventory items including fermentables, hops, yeasts and miscellaneous items.",
)
async def inventory_summary() -> str:
    return await t_inventory.inventory_summary(brewfather_client)


# Batch Endpoints
@mcp.tool(
    name="list_batches",
    description="Lists all brew batches.",
)
async def read_batches_list() -> str:
    return await t_batch.list_batches(brewfather_client)


@mcp.tool(
    name="get_batch_detail",
    description="Get detailed information for a specific batch.",
)
async def read_batch_detail(batch_id: str) -> str:
    return await t_batch.get_batch_detail(brewfather_client, batch_id)


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

    return await t_batch.update_batch(brewfather_client, batch_id, update_data)


# Recipe Endpoints
@mcp.tool(
    name="list_recipes",
    description="Lists all recipes.",
)
async def read_recipes_list() -> str:
    return await t_recipe.list_recipes(brewfather_client)


@mcp.tool(
    name="get_recipe_detail",
    description="Get detailed information for a specific recipe including ingredients, process details and specifications.",
)
async def read_recipe_detail(recipe_id: str) -> str:
    return await t_recipe.get_recipe_detail(brewfather_client, recipe_id)


# Miscellaneous Inventory Endpoints
@mcp.tool(
    name="list_misc_items",
    description="Lists all miscellaneous inventory items.",
)
async def read_miscs_list() -> str:
    return await t_misc.list_misc(brewfather_client)


@mcp.tool(
    name="get_misc_detail",
    description="Get detailed information for a specific miscellaneous inventory item.",
)
async def read_misc_detail(item_id: str) -> str:
    return await t_misc.get_misc_detail(brewfather_client, item_id)


# Inventory Update Tools
@mcp.tool(
    name="update_fermentable_inventory",
    description="Sets the inventory amount for a specific fermentable.",
)
async def update_fermentable_inventory_tool(item_id: str, inventory_amount: float) -> str:
    return await t_fermentable.update_fermentable(brewfather_client, item_id, inventory_amount)


@mcp.tool(
    name="update_hop_inventory",
    description="Sets the inventory amount for a specific hop.",
)
async def update_hop_inventory_tool(item_id: str, inventory_amount: float) -> str:
    return await t_hop.update_hop(brewfather_client, item_id, inventory_amount)


@mcp.tool(
    name="update_misc_inventory",
    description="Sets the inventory amount for a specific miscellaneous item.",
)
async def update_misc_inventory_tool(item_id: str, inventory_amount: float) -> str:
    return await t_misc.update_misc(brewfather_client, item_id, inventory_amount)


@mcp.tool(
    name="update_yeast_inventory",
    description="Sets the inventory amount for a specific yeast.",
)
async def update_yeast_inventory_tool(item_id: str, inventory_amount: float) -> str:
    return await t_yeast.update_yeast(brewfather_client, item_id, inventory_amount)


# Brewtracker endpoints - Enhanced brewing information
@mcp.tool(
    name="get_batch_brewtracker",
    description="Get detailed brewing process guidance and timeline for a batch",
)
async def get_batch_brewtracker(batch_id: str) -> str:
    return await t_batch.get_batch_brewtracker(brewfather_client, batch_id)


@mcp.tool(
    name="get_batch_last_reading",
    description="Get the most recent sensor reading from brewing devices for a batch",
)
async def get_batch_last_reading(batch_id: str) -> str:
    return await t_batch.get_batch_last_reading(brewfather_client, batch_id)


@mcp.tool(
    name="get_batch_readings_summary",
    description="Get a summary of recent sensor readings for a batch (limited to avoid large responses)",
)
async def get_batch_readings_summary(batch_id: str, limit: int = 10) -> str:
    return await t_batch.get_batch_readings_summary(brewfather_client, batch_id, limit)


# Recipe Creation Tools
@mcp.tool(
    name="get_recipe_enums",
    description="Returns valid enum values for recipe creation from defined type system.",
)
async def get_recipe_enums() -> str:
    return t_recipe.get_recipe_enums()


@mcp.tool(
    name="create_recipe",
    description="Creates a complete recipe with ingredients and process steps, returning valid Brewfather JSON for import.",
)
async def create_recipe(
    name: str,
    author: Optional[str] = "MCP Generated",
    recipe_type: Optional[str] = RecipeType.ALL_GRAIN.value,
    style_name: Optional[str] = "Custom Recipe",
    batch_size: Optional[float] = 21.0,
    boil_time: Optional[int] = 60,
    fermentables: Optional[list] = None,
    hops: Optional[list] = None,
    yeasts: Optional[list] = None,
    miscs: Optional[list] = None,
    mash_steps: Optional[list] = None,
    fermentation_temp: Optional[float] = None,
) -> str:
    """
    Creates a recipe with ingredients and process steps.

    Args:
        name: Recipe name (required)
        author: Recipe author (default: "MCP Generated")
        recipe_type: "All Grain", "Extract", or "Partial Mash" (default: "All Grain")
        style_name: Beer style name (default: "Custom Recipe")
        batch_size: Target batch volume in liters (default: 21.0)
        boil_time: Boil duration in minutes (default: 60)
        fermentables: List of fermentable dicts with keys: name, amount (kg), color (optional)
        hops: List of hop dicts with keys: name, amount (g), alpha (%), use, time (min)
        yeasts: List of yeast dicts with keys: name, amount, form (YeastForm values)
        miscs: List of misc dicts with keys: name, amount, use, time (optional)
        mash_steps: List of mash step dicts with keys: stepTemp (°C), stepTime (min), name (optional)
        fermentation_temp: Primary fermentation temperature in °C (optional)

    Returns:
        JSON string formatted for Brewfather import
    """
    logger.info(f"Creating recipe: {name}")

    try:
        # Import here to avoid circular imports
        from brewfather_mcp.types.recipe import RecipeDetail, RecipeStyle
        from brewfather_mcp.types.fermentable import RecipeFermentable
        from brewfather_mcp.types.hop import RecipeHop
        from brewfather_mcp.types.yeast import RecipeYeast
        from brewfather_mcp.types.misc import RecipeMisc
        from brewfather_mcp.types.base import MashSchedule, MashStep, FermentationSchedule, FermentationStep
        import json

        # Validate required fields
        if not name or not name.strip():
            raise ValueError("Recipe name is required")

        # Validate recipe type
        valid_types = [rt.value for rt in RecipeType]
        if recipe_type not in valid_types:
            raise ValueError(f"Invalid recipe type '{recipe_type}'. Valid types: {', '.join(valid_types)}")

        # Set defaults for empty lists
        fermentables = fermentables or []
        hops = hops or []
        yeasts = yeasts or []
        miscs = miscs or []
        mash_steps = mash_steps or []

        # Generate unique recipe ID (simple approach for now)
        import uuid
        recipe_id = str(uuid.uuid4()).replace('-', '')[:22].upper()

        # Create recipe object
        recipe = RecipeDetail(
            _id=recipe_id,
            name=name.strip(),
            author=author.strip() if author else "MCP Generated",
            type=recipe_type,
            batch_size=batch_size,
            boil_time=boil_time,
            style=RecipeStyle(name=style_name or "Custom Recipe"),
            fermentables=[],
            hops=[],
            yeasts=[],
            miscs=[],
            mash=None if not mash_steps else MashSchedule(
                name="Custom Mash Schedule",
                steps=[
                    MashStep(
                        name=step.get("name", ""),
                        stepTemp=step["stepTemp"],
                        stepTime=step["stepTime"],
                        type="Temperature"
                    ) for step in mash_steps
                ]
            ),
            fermentation=FermentationSchedule(
                name="Custom Fermentation Schedule",
                steps=[
                    FermentationStep(
                        stepTemp=fermentation_temp or 20,
                        stepTime=14,  # Default 14 days primary
                        type="Primary"
                    )
                ] if fermentation_temp else []
            ) if fermentation_temp else None
        )

        # Add fermentables
        for ferm_data in fermentables:
            if not ferm_data.get("name") or not ferm_data.get("amount"):
                logger.warning(f"Skipping fermentable with missing name or amount: {ferm_data}")
                continue

            fermentable = RecipeFermentable(
                name=ferm_data["name"],
                type="Grain",  # Default type for fermentables
                amount=float(ferm_data["amount"]),
                color=float(ferm_data.get("color", 3.0)) if ferm_data.get("color") else None,
                id=None  # Let Brewfather assign ID
            )
            recipe.fermentables.append(fermentable)

        # Add hops
        for hop_data in hops:
            if not all(k in hop_data for k in ["name", "amount", "alpha", "use", "time"]):
                logger.warning(f"Skipping hop with missing required fields: {hop_data}")
                continue

            hop = RecipeHop(
                name=hop_data["name"],
                type=HopForm.PELLET,  # Default type for hops
                amount=float(hop_data["amount"]),
                alpha=float(hop_data["alpha"]),
                use=hop_data["use"],
                time=int(hop_data["time"]),
                id=None  # Let Brewfather assign ID
            )
            recipe.hops.append(hop)

        # Add yeasts
        for yeast_data in yeasts:
            if not all(k in yeast_data for k in ["name", "amount", "form"]):
                logger.warning(f"Skipping yeast with missing required fields: {yeast_data}")
                continue

            yeast = RecipeYeast(
                name=yeast_data["name"],
                type=YeastType.ALE,  # Default type for yeast
                amount=float(yeast_data["amount"]),
                form=yeast_data["form"],
                id=None  # Let Brewfather assign ID
            )
            recipe.yeasts.append(yeast)

        # Add miscellaneous ingredients
        for misc_data in miscs:
            if not all(k in misc_data for k in ["name", "amount", "use"]):
                logger.warning(f"Skipping misc with missing required fields: {misc_data}")
                continue

            misc = RecipeMisc(
                name=misc_data["name"],
                amount=float(misc_data["amount"]),
                use=misc_data["use"],
                time=int(misc_data["time"]) if misc_data.get("time") else None,
                id=None  # Let Brewfather assign ID
            )
            recipe.miscs.append(misc)

        # Convert to JSON
        recipe_dict = recipe.model_dump(by_alias=True, exclude_none=True)

        # Clean up the JSON for import - remove calculated fields
        cleanup_fields = [
            'og', 'fg', 'ibu', 'color', 'abv', 'attenuation',
            'buGuRatio', 'rbRatio', 'styleConformity',
            'fermentableIbu', 'extraGravity', 'diastaticPower',
            'sumDryHopPerLiter', 'avgWeightedHopstandTemp',
            'yeastToleranceExceededBy', 'manualFg',
            'hopStandMinutes', 'carbonationStyle'
        ]

        for field in cleanup_fields:
            recipe_dict.pop(field, None)

        json_output = json.dumps(recipe_dict, indent=2, ensure_ascii=False)

        logger.info(f"Successfully created recipe '{name}' with {len(recipe.fermentables)} fermentables, {len(recipe.hops)} hops, {len(recipe.yeasts)} yeasts")

        return f"""RECIPE JSON FOR BREWFATHER IMPORT
====================================

Recipe Name: {name}
Type: {recipe_type}
Batch Size: {batch_size}L
Boil Time: {boil_time} minutes

Ingredients:
- Fermentables: {len(recipe.fermentables)}
- Hops: {len(recipe.hops)}
- Yeasts: {len(recipe.yeasts)}
- Misc: {len(recipe.miscs)}

IMPORT INSTRUCTIONS:
1. Copy the JSON below
2. In Brewfather, go to Recipes → Import → Brewfather JSON
3. Paste the JSON and import

JSON:
-----
{json_output}

Note: Equipment profiles and calculated values (OG, FG, IBU, ABV) will be
set by Brewfather after import. This recipe contains the essential brewing
information needed to make the beer.
"""

    except Exception as e:
        logger.exception(f"Error creating recipe '{name}'")
        raise ValueError(f"Failed to create recipe: {str(e)}")
