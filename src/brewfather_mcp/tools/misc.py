from brewfather_mcp.api import BrewfatherClient, ListQueryParams


async def list_misc(client: BrewfatherClient) -> str:
    params = ListQueryParams()
    params.limit = 50
    data = await client.get_miscs_list(params)

    formatted_response: list[str] = []
    for item in data.root:
        if item.inventory and float(item.inventory) > 0:
            formatted_response.append(
                f"ID: {item.id}\n"
                f"Name: {item.name}\n"
                f"Type: {item.type or 'N/A'}\n"
                f"Inventory: {item.inventory} units (actual unit depends on item)\n"
                f"Notes: {item.notes or 'N/A'}\n"
            )
    return "---\n".join(formatted_response) if formatted_response else "No miscellaneous items found."


async def get_misc_detail(client: BrewfatherClient, item_id: str) -> str:
    item = await client.get_misc_detail(item_id)
    return (
        f"ID: {item.id}\n"
        f"Name: {item.name}\n"
        f"Type: {item.type or 'N/A'}\n"
        f"Inventory: {item.inventory} units\n"
        f"Notes: {item.notes or 'N/A'}\n"
    )


async def update_misc(client: BrewfatherClient, item_id: str, amount: float) -> str:
    await client.update_misc_inventory(item_id, amount)
    return f"Miscellaneous inventory for item {item_id} updated to {amount} units."
