from brewfather_mcp.api import BrewfatherClient, ListQueryParams
from brewfather_mcp.formatter import format_recipe_details
from brewfather_mcp.types.recipe import RecipeType
from brewfather_mcp.types.hop import HopUse, HopForm, HopUsage
from brewfather_mcp.types.yeast import YeastType, Flocculation
from brewfather_mcp.types import YeastForm
from brewfather_mcp.types.misc import MiscUse, MiscType
from brewfather_mcp.types.fermentable import FermentableType, FermentableGrainGroup
from brewfather_mcp.types.base import MashStepType, FermentationStepType


async def list_recipes(client: BrewfatherClient) -> str:
    params = ListQueryParams()
    params.limit = 100
    data = await client.get_recipes_list(params)

    formatted_response: list[str] = []
    for item in data.root:
        formatted_response.append(
            f"ID: {item.id}\n"
            f"Name: {item.name}\n"
            f"Author: {item.author or 'N/A'}\n"
            f"Style: {item.style.name if item.style else 'N/A'}\n"
            f"Type: {item.type or 'N/A'}\n"
        )
    return "---\n".join(formatted_response) if formatted_response else "No recipes found."


async def get_recipe_detail(client: BrewfatherClient, recipe_id: str) -> str:
    item = await client.get_recipe_detail(recipe_id)
    return format_recipe_details(item)


def get_recipe_enums() -> str:
    recipe_types = "\n".join(f"- {rt.value}" for rt in RecipeType)
    hop_uses = "\n".join(f"- {hu.value}" for hu in HopUse)
    hop_forms = "\n".join(f"- {hf.value}" for hf in HopForm)
    hop_usages = "\n".join(f"- {hu.value}" for hu in HopUsage)
    yeast_forms = "\n".join(f"- {yf.value}" for yf in YeastForm)
    yeast_types = "\n".join(f"- {yt.value}" for yt in YeastType)
    flocculation_types = "\n".join(f"- {ft.value}" for ft in Flocculation)
    misc_uses = "\n".join(f"- {mu.value}" for mu in MiscUse)
    misc_types = "\n".join(f"- {mt.value}" for mt in MiscType)
    fermentable_types = "\n".join(f"- {ft.value}" for ft in FermentableType)
    fermentable_grain_groups = "\n".join(f"- {fgg.value}" for fgg in FermentableGrainGroup)
    mash_step_types = "\n".join(f"- {mst.value}" for mst in MashStepType)
    fermentation_step_types = "\n".join(f"- {fst.value}" for fst in FermentationStepType)

    return (
        f"RECIPE ENUM VALUES\n"
        f"=====================================\n\n"
        f"These are the valid enum values you can use when creating recipes.\n\n"
        f"Recipe Types:\n{recipe_types}\n\n"
        f"Hop Uses:\n{hop_uses}\n\n"
        f"Hop Forms:\n{hop_forms}\n\n"
        f"Hop Usage (purpose):\n{hop_usages}\n\n"
        f"Yeast Forms:\n{yeast_forms}\n\n"
        f"Yeast Types:\n{yeast_types}\n\n"
        f"Flocculation Types:\n{flocculation_types}\n\n"
        f"Misc Uses:\n{misc_uses}\n\n"
        f"Misc Types:\n{misc_types}\n\n"
        f"Fermentable Types:\n{fermentable_types}\n\n"
        f"Fermentable Grain Groups:\n{fermentable_grain_groups}\n\n"
        f"Mash Step Types:\n{mash_step_types}\n\n"
        f"Fermentation Step Types:\n{fermentation_step_types}\n"
    )
