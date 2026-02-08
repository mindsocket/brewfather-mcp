from brewfather_mcp.api import BrewfatherClient, ListQueryParams


async def list_hops(client: BrewfatherClient) -> str:
    params = ListQueryParams()
    params.limit = 50
    data = await client.get_hops_list(params)

    formatted_response: list[str] = []
    for item in data.root:
        if item.inventory and float(item.inventory) > 0:
            formatted_response.append(
                f"Identifier: {item.id}\n"
                f"Alpha Acids (A.A): {item.alpha}\n"
                f"Quantity: {item.inventory} grams\n"
                f"Name: {item.name}\n"
                f"Type: {item.type}\n"
                f"Use: {item.use}\n"
            )
    return "---\n".join(formatted_response)


async def get_hop_detail(client: BrewfatherClient, identifier: str) -> str:
    item = await client.get_hop_detail(identifier)
    return (
        f"Name: {item.name}\n"
        f"Type: {item.type}\n"
        f"Origin: {item.origin}\n"
        f"Use: {item.use}\n"
        f"Usage: {item.usage}\n"
        f"Alpha Acid (% A.A): {item.alpha}\n"
        f"Beta: {item.beta}\n"
        f"Inventory: {item.inventory}\n"
        f"Time: {item.time}\n"
        f"IBU: {item.ibu}\n"
        f"Oil: {item.oil}\n"
        f"Myrcene: {item.myrcene}\n"
        f"Caryophyllene: {item.caryophyllene}\n"
        f"Humulene: {item.humulene}\n"
        f"Cohumulone: {item.cohumulone}\n"
        f"Farnesene: {item.farnesene}\n"
        f"HSI: {item.hsi}\n"
        f"Year: {item.year}\n"
        f"Temp: {item.temp}\n"
        f"Amount: {item.amount}\n"
        f"Substitutes: {item.substitutes}\n"
        f"Used In: {item.used_in}\n"
        f"Notes: {item.notes}\n"
        f"User Notes: {item.user_notes}\n"
        f"Hidden: {item.hidden}\n"
        f"Lot Number: {item.lot_number}\n"
        f"Best Before Date: {item.best_before_date}\n"
        f"Manufacturing Date: {item.manufacturing_date}\n"
        f"Version: {item.version}\n"
        f"ID: {item.id}\n"
    )


async def update_hop(client: BrewfatherClient, item_id: str, amount: float) -> str:
    await client.update_hop_inventory(item_id, amount)
    return f"Hop inventory for item {item_id} updated to {amount} grams."
