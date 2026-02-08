from brewfather_mcp.api import BrewfatherClient, ListQueryParams


async def list_yeasts(client: BrewfatherClient) -> str:
    params = ListQueryParams()
    params.limit = 50
    data = await client.get_yeasts_list(params)

    formatted_response: list[str] = []
    for item in data.root:
        if item.inventory and float(item.inventory) > 0:
            formatted_response.append(
                f"Identifier: {item.id}\n"
                f"Attenuation (%): {item.attenuation}\n"
                f"Quantity: {item.inventory} {item.form}\n"
                f"Name: {item.name}\n"
                f"Type: {item.type}\n"
            )
    return "---\n".join(formatted_response)


async def get_yeast_detail(client: BrewfatherClient, identifier: str) -> str:
    item = await client.get_yeast_detail(identifier)
    return (
        f"Name: {item.name}\n"
        f"Type: {item.type}\n"
        f"Form: {item.form}\n"
        f"Laboratory: {item.laboratory}\n"
        f"Product ID: {item.product_id}\n"
        f"Inventory: {item.inventory}\n"
        f"Amount: {item.amount}\n"
        f"Unit: {item.unit}\n"
        f"Attenuation: {item.attenuation}\n"
        f"Min Attenuation: {item.min_attenuation}\n"
        f"Max Attenuation: {item.max_attenuation}\n"
        f"Flocculation: {item.flocculation}\n"
        f"Min Temp: {item.min_temp}\n"
        f"Max Temp: {item.max_temp}\n"
        f"Max ABV: {item.max_abv}\n"
        f"Cells Per Package: {item.cells_per_pkg}\n"
        f"Age Rate: {item.age_rate}\n"
        f"Ferments All: {item.ferments_all}\n"
        f"Description: {item.description}\n"
        f"User Notes: {item.user_notes}\n"
        f"Hidden: {item.hidden}\n"
        f"Best Before Date: {item.best_before_date}\n"
        f"Manufacturing Date: {item.manufacturing_date}\n"
        f"Timestamp: {item.timestamp.seconds if item.timestamp else 'N/A'}\n"
        f"Created: {item.created.seconds if item.created else 'N/A'}\n"
        f"Version: {item.version}\n"
        f"ID: {item.id}\n"
        f"Rev: {item.rev}\n"
    )


async def update_yeast(client: BrewfatherClient, item_id: str, amount: float) -> str:
    await client.update_yeast_inventory(item_id, amount)
    return f"Yeast inventory for item {item_id} updated to {amount} packets."
