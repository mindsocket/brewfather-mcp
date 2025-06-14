from enum import StrEnum
import os
import httpx
import urllib.parse
from .types import (
    FermentableDetail,
    FermentableList,
    HopDetail,
    HopList,
    InventoryCategory,
    MiscDetail,
    MiscList,
    RecipeDetail,
    RecipeList,
    YeastDetail,
    YeastList,
    BatchDetail,
    BatchList,
)

BASE_URL: str = "https://api.brewfather.app/v2"

class OrderByDirection(StrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"

class ListQueryParams:
    inventory_negative: bool | None = None
    complete: bool | None = None
    inventory_exists: bool | None = None
    limit: int | None = None
    start_after: str | None = None
    order_by: str | None = None
    order_by_direction: OrderByDirection | None = None

    def as_query_param_str(self) -> str | None:
        qs = ""

        if self.inventory_negative:
            qs += f"inventory_negative={self.inventory_negative}"

        if self.complete:
            qs += f"complete={self.complete}"
        if self.inventory_exists:
            qs += f"inventory_exists={self.inventory_exists}"

        if self.limit:
            qs += f"limit={self.limit}"

        if self.start_after:
            qs += f"start_after={urllib.parse.quote_plus(self.start_after)}"

        if self.order_by:
            qs += f"order_by={urllib.parse.quote_plus(self.order_by)}"

        if self.order_by_direction:
            qs += f"order_by_direction={self.order_by_direction}"

        if qs:
            return qs
        else:
            return None

class BrewfatherClient:
    """Client for interacting with the Brewfather API."""

    def __init__(self):
        user_id = os.getenv("BREWFATHER_API_USER_ID")
        api_key = os.getenv("BREWFATHER_API_KEY")

        if not user_id or not api_key:
            raise ValueError(
                "Missing Brewfather credentials in the environment variables: BREWFATHER_API_USER_ID or BREWFATHER_API_KEY"
            )

        self.auth = httpx.BasicAuth(user_id, api_key)

    async def _make_request(self, url: str) -> str:
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.get(url)
            response.raise_for_status()
            # Write response to a file for debugging when debug mode is enabled
            if os.getenv("BREWFATHER_MCP_DEBUG"):
                debug_dir = os.path.join(os.path.dirname(__file__), "..", "..", "debug")
                os.makedirs(debug_dir, exist_ok=True)
                debug_filename = url[len(BASE_URL) + 1:].split('?')[0].replace("/", "_").replace(":", "_") + ".json"
                debug_path = os.path.join(debug_dir, debug_filename)
                with open(debug_path, "w") as debug_file:
                    debug_file.write(response.text)
            return response.text

    async def _make_patch_request(self, url: str, data: dict) -> None:
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.patch(url, json=data)
            response.raise_for_status()

    def _build_url(
        self,
        endpoint: str,
        id: str | None = None,
        query_params: ListQueryParams | None = None,
    ) -> str:
        """Build a URL for the Brewfather API.

        Args:
            endpoint: The API endpoint (e.g., 'recipes', 'batches', 'inventory/fermentables')
            id: Optional ID for detail endpoints
            query_params: Optional query parameters
        """
        url = f"{BASE_URL}/{endpoint}"
        if id:
            url = f"{url}/{id}"
        if query_params:
            url += f"?{query_params.as_query_param_str()}"
        return url

    # Inventory endpoints
    async def get_fermentables_list(
        self, query_params: ListQueryParams | None = None
    ) -> FermentableList:
        url = self._build_url(
            f"inventory/{InventoryCategory.FERMENTABLES}", query_params=query_params
        )
        json_response = await self._make_request(url)
        return FermentableList.model_validate_json(json_response)

    async def get_fermentable_detail(self, id: str) -> FermentableDetail:
        url = self._build_url(
            f"inventory/{InventoryCategory.FERMENTABLES}", id=id
        )
        json_response = await self._make_request(url)
        return FermentableDetail.model_validate_json(json_response)

    async def update_fermentable_inventory(self, id: str, inventory: float) -> None:
        url = self._build_url(
            f"inventory/{InventoryCategory.FERMENTABLES}", id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})

    # Batch endpoints
    async def get_batches_list(
        self, query_params: ListQueryParams | None = None
    ) -> BatchList:
        url = self._build_url("batches", query_params=query_params)
        json_response = await self._make_request(url)
        return BatchList.model_validate_json(json_response)

    async def get_batch_detail(self, id: str) -> BatchDetail:
        url = self._build_url("batches", id=id)
        json_response = await self._make_request(url)
        return BatchDetail.model_validate_json(json_response)

    async def update_batch_detail(self, id: str, data: dict) -> None:
        url = self._build_url("batches", id=id)
        await self._make_patch_request(url, data)

    # Recipe endpoints
    async def get_recipes_list(
        self, query_params: ListQueryParams | None = None
    ) -> RecipeList:
        url = self._build_url("recipes", query_params=query_params)
        json_response = await self._make_request(url)
        return RecipeList.model_validate_json(json_response)

    async def get_recipe_detail(self, id: str) -> RecipeDetail:
        url = self._build_url("recipes", id=id)
        json_response = await self._make_request(url)
        return RecipeDetail.model_validate_json(json_response)

    # Add similar patterns for other inventory types (hops, yeasts, miscs)...
    async def get_hops_list(
        self, query_params: ListQueryParams | None = None
    ) -> HopList:
        url = self._build_url(
            f"inventory/{InventoryCategory.HOPS}", query_params=query_params
        )
        json_response = await self._make_request(url)
        return HopList.model_validate_json(json_response)
    
    async def get_hop_detail(self, id: str) -> HopDetail:
        url = self._build_url(
            f"inventory/{InventoryCategory.HOPS}", id=id
        )
        json_response = await self._make_request(url)
        return HopDetail.model_validate_json(json_response)
    
    async def update_hop_inventory(self, id: str, inventory: float) -> None:
        url = self._build_url(
            f"inventory/{InventoryCategory.HOPS}", id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})

    async def get_yeasts_list(
        self, query_params: ListQueryParams | None = None
    ) -> YeastList:
        url = self._build_url(
            f"inventory/{InventoryCategory.YEASTS}", query_params=query_params
        )
        json_response = await self._make_request(url)
        return YeastList.model_validate_json(json_response)
    
    async def get_yeast_detail(self, id: str) -> YeastDetail:
        url = self._build_url(
            f"inventory/{InventoryCategory.YEASTS}", id=id
        )
        json_response = await self._make_request(url)
        return YeastDetail.model_validate_json(json_response)
    
    async def update_yeast_inventory(self, id: str, inventory: float) -> None:
        url = self._build_url(
            f"inventory/{InventoryCategory.YEASTS}", id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})

    async def get_miscs_list(
        self, query_params: ListQueryParams | None = None
    ) -> MiscList:
        url = self._build_url(
            f"inventory/{InventoryCategory.MISCS}", query_params=query_params
        )
        json_response = await self._make_request(url)
        return MiscList.model_validate_json(json_response)

    async def get_misc_detail(self, id: str) -> MiscDetail:
        url = self._build_url(
            f"inventory/{InventoryCategory.MISCS}", id=id
        )
        json_response = await self._make_request(url)
        return MiscDetail.model_validate_json(json_response)
    
    async def update_misc_inventory(self, id: str, inventory: float) -> None:
        url = self._build_url(
            f"inventory/{InventoryCategory.MISCS}", id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})
