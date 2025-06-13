import json
import pytest
import httpx
from respx import MockRouter

from brewfather_mcp.api import BrewfatherClient, BASE_URL
from brewfather_mcp.types import (
    Batch,
    BatchList,
    FermentableDetail,
    FermentableList,
    HopDetail,
    HopList,
    Misc,
    MiscList,
    Recipe,
    RecipeList,
    YeastDetail,
    YeastList,
)


@pytest.fixture
def client(monkeypatch) -> BrewfatherClient:
    """Create a BrewfatherClient instance with mock credentials."""
    monkeypatch.setenv("BREWFATHER_API_USER_ID", "testuser")
    monkeypatch.setenv("BREWFATHER_API_KEY", "testkey")
    return BrewfatherClient()


version_mock = {
    "_rev": "foo",
    "_version": "2.8.1",
    "_timestamp": {"_seconds": 1644033488, "_nanoseconds": 107000000},
    "_timestamp_ms": 1644033488107,
    "_created": {"_seconds": 1621674499, "_nanoseconds": 901000000},
}


@pytest.mark.asyncio
async def test_http_error_handling_get(
    client: BrewfatherClient, respx_mock: MockRouter
):
    respx_mock.get(f"{BASE_URL}/inventory/fermentables").mock(
        return_value=httpx.Response(500)
    )
    with pytest.raises(httpx.HTTPStatusError):
        await client.get_fermentables_list()


@pytest.mark.asyncio
async def test_http_error_handling_patch(
    client: BrewfatherClient, respx_mock: MockRouter
):
    batch_id = "error_batch"
    respx_mock.patch(f"{BASE_URL}/batches/{batch_id}").mock(
        return_value=httpx.Response(401)
    )
    with pytest.raises(httpx.HTTPStatusError):
        await client.update_batch_detail(batch_id, {"status": "Failed"})


class TestFermentables:
    @pytest.mark.asyncio
    async def test_get_fermentables_list(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        mock_data = [
            {
                "_id": "f1",
                "name": "Pilsner Malt",
                "inventory": 10.0,
                "type": "Grain",
                "supplier": "Weyermann",
            }
        ]
        respx_mock.get(f"{BASE_URL}/inventory/fermentables").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_fermentables_list()
        assert isinstance(result, FermentableList)
        assert len(result.root) == 1
        assert result.root[0].id == "f1"
        assert result.root[0].name == "Pilsner Malt"

    @pytest.mark.asyncio
    async def test_get_fermentable_detail(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "f1_detail"
        mock_data = {
            "_id": item_id,
            "name": "CaraPils",
            "inventory": 5.0,
            "potential": 1.035,
            "type": "Grain",
            "supplier": "Briess",
            "color": 2.0,
            "potentialPercentage": 80.0,
            "potential": 1.035,
        } | version_mock
        respx_mock.get(f"{BASE_URL}/inventory/fermentables/{item_id}").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_fermentable_detail(item_id)
        assert isinstance(result, FermentableDetail)
        assert result.id == item_id
        assert result.potential == 1.035

    @pytest.mark.asyncio
    async def test_update_fermentable_inventory(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "f_inv_update"
        inventory_amount = 25.5
        respx_mock.patch(f"{BASE_URL}/inventory/fermentables/{item_id}").mock(
            return_value=httpx.Response(200)
        )
        await client.update_fermentable_inventory(item_id, inventory_amount)
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls.last.request
        assert request.method == "PATCH"
        assert json.loads(request.content) == {"inventory": inventory_amount}


class TestHops:
    @pytest.mark.asyncio
    async def test_get_hops_list(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        mock_data = [
            {
                "_id": "h1",
                "name": "Cascade",
                "inventory": 200.0,
                "alpha": 5.5,
                "type": "Pellet",
            }
        ]
        respx_mock.get(f"{BASE_URL}/inventory/hops").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_hops_list()
        assert isinstance(result, HopList)
        assert len(result.root) == 1
        assert result.root[0].name == "Cascade"

    @pytest.mark.asyncio
    async def test_get_hop_detail(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "h1_detail"
        mock_data = {
            "_id": item_id,
            "name": "Citra",
            "inventory": 100.0,
            "alpha": 12.0,
            "type": "Pellet",
            "use": "Aroma",
        } | version_mock
        respx_mock.get(f"{BASE_URL}/inventory/hops/{item_id}").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_hop_detail(item_id)
        assert isinstance(result, HopDetail)
        assert result.alpha == 12.0

    @pytest.mark.asyncio
    async def test_update_hop_inventory(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "h_inv_update"
        inventory_amount = 150.0
        respx_mock.patch(f"{BASE_URL}/inventory/hops/{item_id}").mock(
            return_value=httpx.Response(200)
        )
        await client.update_hop_inventory(item_id, inventory_amount)
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls.last.request
        assert json.loads(request.content) == {"inventory": inventory_amount}


class TestYeasts:
    @pytest.mark.asyncio
    async def test_get_yeasts_list(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        mock_data = [
            {
                "_id": "y1",
                "name": "US-05",
                "inventory": 5.0,
                "attenuation": 81,
                "type": "Ale",
            }
        ]
        respx_mock.get(f"{BASE_URL}/inventory/yeasts").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_yeasts_list()
        assert isinstance(result, YeastList)
        assert len(result.root) == 1
        assert result.root[0].attenuation == 81

    @pytest.mark.asyncio
    async def test_get_yeast_detail(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "y1_detail"
        mock_data = {
            "_id": item_id,
            "name": "WLP001",
            "inventory": 2.0,
            "attenuation": 78,
            "laboratory": "White Labs",
            "type": "Ale",
        } | version_mock
        respx_mock.get(f"{BASE_URL}/inventory/yeasts/{item_id}").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_yeast_detail(item_id)
        assert isinstance(result, YeastDetail)
        assert result.laboratory == "White Labs"

    @pytest.mark.asyncio
    async def test_update_yeast_inventory(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "y_inv_update"
        inventory_amount = 10.0
        respx_mock.patch(f"{BASE_URL}/inventory/yeasts/{item_id}").mock(
            return_value=httpx.Response(200)
        )
        await client.update_yeast_inventory(item_id, inventory_amount)
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls.last.request
        assert json.loads(request.content) == {"inventory": inventory_amount}


class TestBatches:
    @pytest.mark.asyncio
    async def test_get_batches_list_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        mock_response_data = [
            {
                "_id": "batch1",
                "name": "Test Batch",
                "batchNo": 1,
                "recipe": {"name": "Test Recipe"},
            }
        ]
        respx_mock.get(f"{BASE_URL}/batches").mock(
            return_value=httpx.Response(200, json=mock_response_data)
        )
        result = await client.get_batches_list()
        assert isinstance(result, BatchList)
        assert len(result.root) == 1
        assert result.root[0].id == "batch1"
        assert result.root[0].name == "Test Batch"

    @pytest.mark.asyncio
    async def test_get_batches_list_empty(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        respx_mock.get(f"{BASE_URL}/batches").mock(
            return_value=httpx.Response(200, json=[])
        )
        result = await client.get_batches_list()
        assert isinstance(result, BatchList)
        assert len(result.root) == 0

    @pytest.mark.asyncio
    async def test_get_batch_detail_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        batch_id = "b_detail"
        mock_data = {
            "_id": batch_id,
            "name": "Detailed Batch",
            "status": "Fermenting",
            "recipe": {"name": "Detailed Recipe"},
            "batchNo": 2,
        } | version_mock
        respx_mock.get(f"{BASE_URL}/batches/{batch_id}").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_batch_detail(batch_id)
        assert isinstance(result, Batch)
        assert result.id == batch_id
        assert result.status == "Fermenting"

    @pytest.mark.asyncio
    async def test_update_batch_detail_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        batch_id = "b_update"
        payload = {"status": "Completed", "measuredFg": 1.010}
        respx_mock.patch(f"{BASE_URL}/batches/{batch_id}").mock(
            return_value=httpx.Response(200)
        )
        await client.update_batch_detail(batch_id, payload)
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls.last.request
        assert request.method == "PATCH"
        assert str(request.url) == f"{BASE_URL}/batches/{batch_id}"
        assert json.loads(request.content) == payload


class TestRecipes:
    @pytest.mark.asyncio
    async def test_get_recipes_list_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        mock_data = [{"_id": "r1", "name": "My IPA", "type": "All Grain"}]
        respx_mock.get(f"{BASE_URL}/recipes").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_recipes_list()
        assert isinstance(result, RecipeList)
        assert len(result.root) == 1
        assert result.root[0].name == "My IPA"

    @pytest.mark.asyncio
    async def test_get_recipe_detail_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        recipe_id = "r_detail"
        mock_data = {
            "_id": recipe_id,
            "name": "Detailed Recipe",
            "author": "Brewer Joe",
        }
        respx_mock.get(f"{BASE_URL}/recipes/{recipe_id}").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_recipe_detail(recipe_id)
        assert isinstance(result, Recipe)
        assert result.id == recipe_id
        assert result.author == "Brewer Joe"


class TestMiscellaneous:
    @pytest.mark.asyncio
    async def test_get_miscs_list_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        mock_data = [
            {"_id": "m1", "name": "Irish Moss", "inventory": 50.0, "type": "Fining"}
        ]
        respx_mock.get(f"{BASE_URL}/inventory/miscs").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_miscs_list()
        assert isinstance(result, MiscList)
        assert len(result.root) == 1
        assert result.root[0].type == "Fining"

    @pytest.mark.asyncio
    async def test_get_misc_detail_success(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "m_detail"
        mock_data = {
            "_id": item_id,
            "name": "Whirlfloc",
            "notes": "Use 1 tablet per 5 gallons",
        } | version_mock
        respx_mock.get(f"{BASE_URL}/inventory/miscs/{item_id}").mock(
            return_value=httpx.Response(200, json=mock_data)
        )
        result = await client.get_misc_detail(item_id)
        assert isinstance(result, Misc)
        assert result.id == item_id
        assert result.notes == "Use 1 tablet per 5 gallons"

    @pytest.mark.asyncio
    async def test_update_misc_inventory(
        self, client: BrewfatherClient, respx_mock: MockRouter
    ):
        item_id = "m_inv_update"
        inventory_amount = 20.0
        respx_mock.patch(f"{BASE_URL}/inventory/miscs/{item_id}").mock(
            return_value=httpx.Response(200)
        )
        await client.update_misc_inventory(item_id, inventory_amount)
        assert len(respx_mock.calls) == 1
        request = respx_mock.calls.last.request
        assert json.loads(request.content) == {"inventory": inventory_amount}
