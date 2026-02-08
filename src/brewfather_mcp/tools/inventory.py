from brewfather_mcp.api import BrewfatherClient
from brewfather_mcp.inventory import (
    get_fermentables_summary,
    get_hops_summary,
    get_yeast_summary,
    get_miscs_summary,
)


async def inventory_summary(client: BrewfatherClient) -> str:
    fermentables = await get_fermentables_summary(client)
    hops = await get_hops_summary(client)
    yeasts = await get_yeast_summary(client)
    miscs = await get_miscs_summary(client)

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

    response += "\n---\n"

    response += "Miscellaneous Items:\n\n"
    for misc in miscs:
        for k, v in misc.items():
            response += f"{k}: {v}\n"
        response += "\n"

    return response
