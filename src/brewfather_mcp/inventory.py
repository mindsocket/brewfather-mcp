from brewfather_mcp.api import BrewfatherClient
from brewfather_mcp.utils import AnyDictList, empty_if_null, get_in_batches

async def get_fermentables_summary(
    brewfather_client: BrewfatherClient,
) -> AnyDictList:
    fermentables_data = await brewfather_client.get_fermentables_list()

    detail_results = await get_in_batches(
        3,
        brewfather_client.get_fermentable_detail,
        fermentables_data,
    )

    fermentables: AnyDictList = []
    for f_data, fermentable_data in zip(
        fermentables_data.root, detail_results, strict=True
    ):
        fermentable_data = await brewfather_client.get_fermentable_detail(f_data.id)

        fermentables.append(
            {
                "Name": f_data.name,
                "Type": f_data.type,
                "Yield": empty_if_null(fermentable_data.friability),
                "Lot #": empty_if_null(fermentable_data.lot_number),
                "Best Before Date": empty_if_null(fermentable_data.best_before_date),
                "Inventory Amount": f"{fermentable_data.inventory} kg",
            }
        )

    return fermentables


async def get_hops_summary(brewfather_client: BrewfatherClient) -> AnyDictList:
    hops_data = await brewfather_client.get_hops_list()
    detail_results = await get_in_batches(
        3, brewfather_client.get_hop_detail, hops_data
    )

    hops: AnyDictList = []
    for h_data, hop_data in zip(hops_data.root, detail_results, strict=True):
        hops.append(
            {
                "Name": h_data.name,
                "Year": empty_if_null(hop_data.year),
                "Alpha Acid": h_data.alpha,
                "Lot #": empty_if_null(hop_data.lot_number),
                "Best Before Date": empty_if_null(hop_data.best_before_date),
                "Inventory Amount": f"{hop_data.inventory} grams",
            }
        )

    return hops


async def get_yeast_summary(
    brewfather_client: BrewfatherClient,
) -> AnyDictList:
    yeasts_data = await brewfather_client.get_yeasts_list()
    detail_results = await get_in_batches(
        3, brewfather_client.get_yeast_detail, yeasts_data
    )

    yeasts: AnyDictList = []
    for y_data, yeast_data in zip(yeasts_data.root, detail_results, strict=True):
        yeasts.append(
            {
                "Name": y_data.name,
                "Form": yeast_data.form,
                "Attenuation": f"{y_data.attenuation}%",
                "Lot #": empty_if_null(yeast_data.lot_number),
                "Best Before Date": empty_if_null(yeast_data.best_before_date),
                "Inventory Amount": f"{yeast_data.inventory} pkg",
            }
        )

    return yeasts


async def get_miscs_summary(
    brewfather_client: BrewfatherClient,
) -> AnyDictList:
    """Get a summary of miscellaneous inventory items.

    Args:
        brewfather_client: The Brewfather API client instance.

    Returns:
        A list of dictionaries containing summarized miscellaneous item information.
    """
    miscs_data = await brewfather_client.get_miscs_list()
    detail_results = await get_in_batches(
        3, brewfather_client.get_misc_detail, miscs_data
    )

    miscs: AnyDictList = []
    for m_data, misc_data in zip(
        miscs_data.root, detail_results, strict=True
    ):
        miscs.append(
            {
                "Name": m_data.name,
                "Type": m_data.type or "N/A",
                "Notes": empty_if_null(misc_data.notes),
                "Inventory Amount": f"{misc_data.inventory} units",
            }
        )

    return miscs
