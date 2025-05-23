import os

import httpx

from brewfather_mcp.types import (
    FermentableDetail,
    FermentableList,
    HopDetail,
    HopList,
    InventoryCategory,
    ListQueryParams,
    Miscellaneous,
    MiscellaneousList,
    Recipe,
    RecipeList,
    YeastDetail,
    YeastList,
    Batch,
    BatchList,
)

BASE_URL: str = "https://api.brewfather.app/v2"


class BrewfatherInventoryClient:
    __prefix: str = "/inventory"
    __base_url: str = f"{BASE_URL}{__prefix}"
    __inventory_summary_url: str = f"{__base_url}/{{category}}"
    __inventory_detail_url: str = f"{__base_url}/{{category}}/{{id}}"

    auth: httpx.BasicAuth

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
            return response.text

    async def _make_patch_request(self, url: str, data: dict) -> None:
        async with httpx.AsyncClient(auth=self.auth) as client:
            response = await client.patch(url, json=data)
            response.raise_for_status()

    async def get_fermentables_list(
        self, query_params: ListQueryParams | None = None
    ) -> FermentableList:
        url = self.__inventory_summary_url.format(
            category=InventoryCategory.FERMENTABLES
        )

        if query_params:
            url += f"?{query_params.as_query_param_str()}"

        json_response = await self._make_request(url)
        return FermentableList.model_validate_json(json_response)

    async def get_fermentable_detail(self, id: str) -> FermentableDetail:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.FERMENTABLES, id=id
        )
        json_response = await self._make_request(url)
        return FermentableDetail.model_validate_json(json_response)

    async def get_hops_list(
        self, query_params: ListQueryParams | None = None
    ) -> HopList:
        url = self.__inventory_summary_url.format(category=InventoryCategory.HOPS)

        if query_params:
            url += f"?{query_params.as_query_param_str()}"

        json_response = await self._make_request(url)
        return HopList.model_validate_json(json_response)

    async def get_hop_detail(self, id: str) -> HopDetail:
        url = self.__inventory_detail_url.format(category=InventoryCategory.HOPS, id=id)
        json_response = await self._make_request(url)
        return HopDetail.model_validate_json(json_response)

    async def get_yeasts_list(
        self, query_params: ListQueryParams | None = None
    ) -> YeastList:
        url = self.__inventory_summary_url.format(category=InventoryCategory.YEASTS)

        if query_params:
            url += f"?{query_params.as_query_param_str()}"

        json_response = await self._make_request(url)
        return YeastList.model_validate_json(json_response)

    async def get_yeast_detail(self, id: str) -> YeastDetail:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.YEASTS, id=id
        )
        json_response = await self._make_request(url)
        return YeastDetail.model_validate_json(json_response)

    async def get_batches_list(
        self, query_params: ListQueryParams | None = None
    ) -> BatchList:
        url = f"{BASE_URL}/batches"
        if query_params:
            url += f"?{query_params.as_query_param_str()}"
        json_response = await self._make_request(url)
        return BatchList.model_validate_json(json_response)

    async def get_batch_detail(self, id: str) -> Batch:
        url = f"{BASE_URL}/batches/{id}"
        json_response = await self._make_request(url)
        return Batch.model_validate_json(json_response)

    async def update_batch_detail(self, id: str, data: dict) -> None:
        url = f"{BASE_URL}/batches/{id}"
        await self._make_patch_request(url, data)

    async def get_recipes_list(
        self, query_params: ListQueryParams | None = None
    ) -> RecipeList:
        url = f"{BASE_URL}/recipes"
        if query_params:
            url += f"?{query_params.as_query_param_str()}"
        json_response = await self._make_request(url)
        return RecipeList.model_validate_json(json_response)

    async def get_recipe_detail(self, id: str) -> Recipe:
        url = f"{BASE_URL}/recipes/{id}"
        json_response = await self._make_request(url)
        return Recipe.model_validate_json(json_response)

    async def get_miscs_list(
        self, query_params: ListQueryParams | None = None
    ) -> MiscellaneousList:
        url = self.__inventory_summary_url.format(
            category=InventoryCategory.MISCELLANEOUS
        )
        if query_params:
            url += f"?{query_params.as_query_param_str()}"
        json_response = await self._make_request(url)
        return MiscellaneousList.model_validate_json(json_response)

    async def get_misc_detail(self, id: str) -> Miscellaneous:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.MISCELLANEOUS, id=id
        )
        json_response = await self._make_request(url)
        return Miscellaneous.model_validate_json(json_response)

    async def update_fermentable_inventory(self, id: str, inventory: float) -> None:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.FERMENTABLES, id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})

    async def update_hop_inventory(self, id: str, inventory: float) -> None:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.HOPS, id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})

    async def update_misc_inventory(self, id: str, inventory: float) -> None:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.MISCELLANEOUS, id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})

    async def update_yeast_inventory(self, id: str, inventory: float) -> None:
        url = self.__inventory_detail_url.format(
            category=InventoryCategory.YEASTS, id=id
        )
        await self._make_patch_request(url, {"inventory": inventory})
