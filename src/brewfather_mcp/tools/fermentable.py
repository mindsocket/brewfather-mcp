from brewfather_mcp.api import BrewfatherClient, ListQueryParams


async def list_fermentables(client: BrewfatherClient) -> str:
    params = ListQueryParams()
    params.limit = 50
    data = await client.get_fermentables_list(params)

    formatted_response: list[str] = []
    for item in data.root:
        if item.inventory and float(item.inventory) > 0:
            formatted_response.append(
                f"Name: {item.name}\n"
                f"Type: {item.type}\n"
                f"Supplier: {item.supplier}\n"
                f"Quantity: {item.inventory} kg\n"
                f"Identifier: {item.id}\n"
            )
    return "---\n".join(formatted_response)


async def get_fermentable_detail(client: BrewfatherClient, identifier: str) -> str:
    item = await client.get_fermentable_detail(identifier)
    return (
        f"Name: {item.name}\n"
        f"Type: {item.type}\n"
        f"Supplier: {item.supplier}\n"
        f"Inventory: {item.inventory}\n"
        f"Origin: {item.origin}\n"
        f"Grain Category: {item.grain_category}\n"
        f"Potential: {item.potential}\n"
        f"Potential Percentage: {item.potential_percentage}\n"
        f"Color: {item.color}\n"
        f"Moisture: {item.moisture}\n"
        f"Protein: {item.protein}\n"
        f"Diastatic Power: {item.diastatic_power}\n"
        f"Friability: {item.friability}\n"
        f"Not Fermentable: {item.not_fermentable}\n"
        f"Max In Batch: {item.max_in_batch}\n"
        f"Coarse Fine Diff: {item.coarse_fine_diff}\n"
        f"Percent Extract Fine-Ground Dry Basis (FGDB): {item.fgdb}\n"
        f"Hidden: {item.hidden}\n"
        f"Notes: {item.notes}\n"
        f"User Notes: {item.user_notes}\n"
        f"Used In: {item.used_in}\n"
        f"Substitutes: {item.substitutes}\n"
        f"Cost Per Amount: {item.cost_per_amount}\n"
        f"Best Before Date: {item.best_before_date}\n"
        f"Manufacturing Date: {item.manufacturing_date}\n"
        f"Free Amino Nitrogen (FAN): {item.fan}\n"
        f"Percent Coarse-Ground Dry Basic (CGDB): {item.cgdb}\n"
        f"Acid: {item.acid}\n"
        f"ID: {item.id}\n"
    )


async def update_fermentable(client: BrewfatherClient, item_id: str, amount: float) -> str:
    await client.update_fermentable_inventory(item_id, amount)
    return f"Fermentable inventory for item {item_id} updated to {amount} kg."
